import urllib.request
import urllib.parse
import json
import csv
import os
import re
import unicodedata
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional: USDA API key from environment variable (if set)
USDA_API_KEY = os.getenv('USDA_API_KEY')  # Note: reading env is allowed; avoid .env files per project rule


# ---------------------------------------------------------------------------
# Fuzzy relevance scoring
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase, strip accents, collapse whitespace, remove punctuation."""
    text = text.lower().strip()
    # Remove accents (for latin chars; cyrillic stays as-is)
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    # Remove punctuation except spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _common_prefix_len(a: str, b: str) -> int:
    """Return the length of the common prefix between two strings."""
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    return i


def _relevance_score(query: str, name: str) -> float:
    """Return a relevance score between 0.0 (no match) and 1.0 (perfect match).

    Scoring strategy:
    - Exact match → 1.0
    - Substring match (either way) → generous base score
    - Token overlap → reward partial matches based on matching words
    """
    q = _normalize(query)
    n = _normalize(name)

    if not q or not n:
        return 0.0

    if q == n:
        return 1.0

    score = 0.0

    # Substring matching
    if q in n:
        score += 0.5
        if n.startswith(q):
            score += 0.2
    elif n in q:
        score += 0.3

    q_tokens = q.split()
    n_tokens = n.split()

    if q_tokens and n_tokens:
        # Exact token overlap
        q_set = set(q_tokens)
        n_set = set(n_tokens)
        intersection = q_set & n_set
        
        if intersection:
            # Reward having any exact matching word (e.g. "филе" in "курица филе")
            overlap_ratio = len(intersection) / len(q_set)
            score += 0.4 * overlap_ratio
        
        # Stem/prefix matching for words that don't match exactly
        unmatched_q = q_set - intersection
        unmatched_n = n_set - intersection
        
        if unmatched_q and unmatched_n:
            prefix_matches = 0
            for qt in unmatched_q:
                best_prefix_len = 0
                for nt in unmatched_n:
                    cp = _common_prefix_len(qt, nt)
                    min_len = min(len(qt), len(nt))
                    if min_len >= 3 and cp >= min(4, min_len):
                        best_prefix_len = max(best_prefix_len, cp)
                if best_prefix_len > 0:
                    prefix_matches += 1
            
            if prefix_matches > 0:
                score += 0.3 * (prefix_matches / len(q_set))

    return min(score, 1.0)


# ---------------------------------------------------------------------------
# Provider: Open Food Facts (world — tags_lc=ru for better cyrillic search)
# ---------------------------------------------------------------------------

def _search_openfoodfacts(query: str) -> List[Dict]:
    """Search Open Food Facts with tags locale set to Russian."""
    if not query:
        return []
    encoded = urllib.parse.quote_plus(query.strip())
    url = (
        f"https://world.openfoodfacts.org/cgi/search.pl?"
        f"search_terms={encoded}&search_simple=1&action=process"
        f"&json=1&page_size=50&lc=ru&tags_lc=ru"
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'CulinaryNavigator/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return []
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return []
    return _parse_off_products(data)


# ---------------------------------------------------------------------------
# Provider: Open Food Facts (Russian subdomain)
# ---------------------------------------------------------------------------

def _search_openfoodfacts_ru(query: str) -> List[Dict]:
    """Search Open Food Facts via the Russian subdomain for better RU results."""
    if not query:
        return []
    encoded = urllib.parse.quote_plus(query.strip())
    url = (
        f"https://ru.openfoodfacts.org/cgi/search.pl?"
        f"search_terms={encoded}&search_simple=1&action=process"
        f"&json=1&page_size=50&lc=ru&tags_lc=ru"
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'CulinaryNavigator/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return []
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return []
    return _parse_off_products(data, source='openfoodfacts_ru')


def _parse_off_products(data: dict, source: str = 'openfoodfacts') -> List[Dict]:
    """Parse Open Food Facts API response into our standard product format."""
    results = []
    for prod in data.get('products', []):
        # Try multiple name fields, prefer Russian
        name = (
            prod.get('product_name_ru')
            or prod.get('product_name')
            or prod.get('generic_name_ru')
            or prod.get('generic_name')
        )
        if not name or not name.strip():
            continue
        nutr = prod.get('nutriments', {})
        calories = nutr.get('energy-kcal_100g')
        if calories is None:
            energy = nutr.get('energy_100g')
            if energy is not None:
                try:
                    calories = float(energy) / 4.184
                except Exception:
                    calories = 0.0
            else:
                calories = 0.0
        proteins = nutr.get('proteins_100g') or 0.0
        fats = nutr.get('fat_100g') or nutr.get('fats_100g') or 0.0
        carbs = nutr.get('carbohydrates_100g') or 0.0

        # Also store categories for extra relevance hints
        categories = (
            prod.get('categories_tags_ru')
            or prod.get('categories')
            or prod.get('categories_tags')
            or ''
        )
        if isinstance(categories, list):
            categories = ' '.join(categories)

        results.append({
            'name': str(name).strip()[:100],
            'calories': round(float(calories), 1),
            'proteins': round(float(proteins), 1),
            'fats': round(float(fats), 1),
            'carbohydrates': round(float(carbs), 1),
            '_source': source,
            '_categories': str(categories).lower(),
        })
    return results


# ---------------------------------------------------------------------------
# Provider: USDA FoodData Central
# ---------------------------------------------------------------------------

def _search_usda(query: str) -> List[Dict]:
    """Search USDA FoodData Central. Requires API key; if not present, returns empty list."""
    if not query or not USDA_API_KEY:
        return []
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={USDA_API_KEY}&query={encoded}&pageSize=25"
    req = urllib.request.Request(url, headers={'User-Agent': 'CulinaryNavigator/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return []
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return []
    results = []
    for food in data.get('foods', []):
        name = food.get('description')
        if not name:
            continue
        nutrients = {n.get('nutrientName', '').lower(): n.get('value', 0) for n in food.get('foodNutrients', [])}
        calories = nutrients.get('energy', 0.0)
        proteins = nutrients.get('protein', 0.0)
        fats = nutrients.get('total lipid (fat)', 0.0)
        carbs = nutrients.get('carbohydrate, by difference', 0.0)
        results.append({
            'name': str(name).strip()[:100],
            'calories': round(float(calories), 1),
            'proteins': round(float(proteins), 1),
            'fats': round(float(fats), 1),
            'carbohydrates': round(float(carbs), 1),
            '_source': 'usda',
            '_categories': '',
        })
    return results


# ---------------------------------------------------------------------------
# Provider: Calorizator.ru
# ---------------------------------------------------------------------------

def _search_calorizator(query: str) -> List[Dict]:
    """Search calorizator.ru auto-complete endpoint for Russian product КБЖУ data."""
    if not query:
        return []
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://calorizator.ru/ajax/product-search?query={encoded}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'CulinaryNavigator/1.0',
        'Accept': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return []
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return []
    results = []
    items = data if isinstance(data, list) else data.get('suggestions', data.get('results', data.get('items', [])))
    if not isinstance(items, list):
        return []
    for item in items:
        if isinstance(item, dict):
            name = item.get('name') or item.get('value') or item.get('title', '')
            if not name:
                continue
            try:
                calories = float(item.get('calories', item.get('cal', 0)) or 0)
                proteins = float(item.get('proteins', item.get('protein', 0)) or 0)
                fats = float(item.get('fats', item.get('fat', 0)) or 0)
                carbs = float(item.get('carbohydrates', item.get('carbs', 0)) or 0)
            except (ValueError, TypeError):
                continue
            results.append({
                'name': str(name).strip()[:100],
                'calories': round(calories, 1),
                'proteins': round(proteins, 1),
                'fats': round(fats, 1),
                'carbohydrates': round(carbs, 1),
                '_source': 'calorizator',
                '_categories': '',
            })
    return results


# ---------------------------------------------------------------------------
# Provider: Local CSV fallback
# ---------------------------------------------------------------------------

def _search_local_csv(query: str) -> List[Dict]:
    """Search a static CSV file bundled with the project.
    Uses substring and stem/prefix matching for better recall.
    Expected CSV columns: name,calories,proteins,fats,carbohydrates
    """
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'fallback_products.csv')
    if not os.path.isfile(csv_path):
        return []
    results = []
    q = query.lower().strip()
    q_tokens = q.split()
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name', '')
                name_lower = name.lower()
                matched = False

                # Direct substring match
                if q in name_lower:
                    matched = True
                else:
                    # Token prefix matching: each query token must match
                    # a prefix (>= 4 chars) of at least one name token
                    name_tokens = name_lower.split()
                    all_matched = True
                    for qt in q_tokens:
                        token_ok = False
                        for nt in name_tokens:
                            cp = _common_prefix_len(qt, nt)
                            if cp >= min(4, min(len(qt), len(nt))):
                                token_ok = True
                                break
                        if not token_ok:
                            all_matched = False
                            break
                    if all_matched and q_tokens:
                        matched = True

                if matched:
                    results.append({
                        'name': name[:100],
                        'calories': round(float(row.get('calories', 0)), 1),
                        'proteins': round(float(row.get('proteins', 0)), 1),
                        'fats': round(float(row.get('fats', 0)), 1),
                        'carbohydrates': round(float(row.get('carbohydrates', 0)), 1),
                        '_source': 'local_csv',
                        '_categories': '',
                    })
    except Exception:
        return []
    return results


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _dedup_key(item: Dict) -> str:
    """Create a dedup key from normalized name + rounded macros."""
    n = _normalize(item.get('name', ''))
    # Include rounded macros to distinguish truly different products with similar names
    cal = round(item.get('calories', 0) / 10) * 10  # bucket by ~10 kcal
    return f"{n}|{cal}"


def _deduplicate(items: List[Dict]) -> List[Dict]:
    """Remove near-duplicate entries, preferring items that appeared earlier (higher-scored)."""
    seen = {}
    result = []
    for item in items:
        key = _dedup_key(item)
        if key not in seen:
            seen[key] = True
            result.append(item)
    return result


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

_ALL_PROVIDERS = [
    _search_openfoodfacts,
    _search_openfoodfacts_ru,
    _search_usda,
    _search_calorizator,
    _search_local_csv,
]

# Minimum relevance threshold — results below this are discarded
_MIN_RELEVANCE = 0.05


def search_products(query: str) -> List[Dict]:
    """Query ALL providers in parallel, merge results, rank by relevance, deduplicate.
    Returns the top 30 most relevant matches.
    To prevent 503 errors from external APIs on multi-word queries, we query using
    the most significant word (longest token) and then apply full query relevance scoring locally.
    """
    if not query or len(query.strip()) < 2:
        return []

    original_query = query.strip()
    
    # Extract the most significant word to send to external APIs
    tokens = [t for t in _normalize(original_query).split() if len(t) >= 2]
    if not tokens:
        return []
        
    # Use the longest word as the primary API search term (e.g. "курица" from "курица филе")
    api_query = max(tokens, key=len)
    
    all_results: List[Dict] = []

    # Run all providers concurrently using the optimized api_query
    with ThreadPoolExecutor(max_workers=len(_ALL_PROVIDERS)) as executor:
        futures = {executor.submit(fn, api_query): fn.__name__ for fn in _ALL_PROVIDERS}
        for future in as_completed(futures):
            try:
                results = future.result(timeout=10)
                if results:
                    all_results.extend(results)
            except Exception:
                pass  # Provider failed — skip silently

    if not all_results:
        return []

    # Score each result by relevance to the FULL ORIGINAL query
    scored: List[Tuple[float, Dict]] = []
    for item in all_results:
        name = item.get('name', '')
        score = _relevance_score(original_query, name)

        # If name doesn't match, check categories
        categories = item.get('_categories', '')
        if score < _MIN_RELEVANCE and categories:
            cat_score = _relevance_score(original_query, categories)
            score = max(score, cat_score * 0.4)

        if item.get('calories', 0) > 0:
            score += 0.02

        scored.append((score, item))

    # Filter out irrelevant results
    scored = [(s, item) for s, item in scored if s >= _MIN_RELEVANCE]

    if not scored:
        return []

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Flatten and deduplicate
    sorted_items = [item for _, item in scored]
    deduped = _deduplicate(sorted_items)

    # Remove internal keys before returning
    for item in deduped:
        item.pop('_source', None)
        item.pop('_categories', None)

    return deduped[:30]
