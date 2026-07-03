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


def _relevance_score(query: str, name: str) -> float:
    """Return a relevance score between 0.0 (no match) and 1.0 (perfect match).
    Uses token overlap plus substring bonus.
    """
    q = _normalize(query)
    n = _normalize(name)

    if not q or not n:
        return 0.0

    # Exact match
    if q == n:
        return 1.0

    score = 0.0

    # Substring bonus: query is contained in name or vice versa
    if q in n:
        score += 0.5
    elif n in q:
        score += 0.4

    # Token overlap (Jaccard-like)
    q_tokens = set(q.split())
    n_tokens = set(n.split())
    if q_tokens and n_tokens:
        intersection = q_tokens & n_tokens
        union = q_tokens | n_tokens
        jaccard = len(intersection) / len(union)
        score += 0.5 * jaccard

    return min(score, 1.0)


# ---------------------------------------------------------------------------
# Provider: Open Food Facts
# ---------------------------------------------------------------------------

def _search_openfoodfacts(query: str) -> List[Dict]:
    """Search Open Food Facts (Russian locale)"""
    if not query:
        return []
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={encoded}&search_simple=1&action=process&json=1&page_size=25&lc=ru"
    req = urllib.request.Request(url, headers={'User-Agent': 'CulinaryNavigator/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return []
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return []
    results = []
    for prod in data.get('products', []):
        name = prod.get('product_name_ru') or prod.get('product_name')
        if not name:
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
        results.append({
            'name': str(name).strip()[:100],
            'calories': round(float(calories), 1),
            'proteins': round(float(proteins), 1),
            'fats': round(float(fats), 1),
            'carbohydrates': round(float(carbs), 1),
            '_source': 'openfoodfacts',
        })
    return results


# ---------------------------------------------------------------------------
# Provider: Open Food Facts (Russian subdomain — better for cyrillic queries)
# ---------------------------------------------------------------------------

def _search_openfoodfacts_ru(query: str) -> List[Dict]:
    """Search Open Food Facts via the Russian subdomain for better RU results."""
    if not query:
        return []
    encoded = urllib.parse.quote_plus(query.strip())
    url = f"https://ru.openfoodfacts.org/cgi/search.pl?search_terms={encoded}&search_simple=1&action=process&json=1&page_size=25&lc=ru"
    req = urllib.request.Request(url, headers={'User-Agent': 'CulinaryNavigator/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return []
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return []
    results = []
    for prod in data.get('products', []):
        name = prod.get('product_name_ru') or prod.get('product_name')
        if not name:
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
        results.append({
            'name': str(name).strip()[:100],
            'calories': round(float(calories), 1),
            'proteins': round(float(proteins), 1),
            'fats': round(float(fats), 1),
            'carbohydrates': round(float(carbs), 1),
            '_source': 'openfoodfacts_ru',
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
        })
    return results


# ---------------------------------------------------------------------------
# Provider: Calorizator.ru (scrape-like JSON endpoint for Russian products)
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
            })
    return results


# ---------------------------------------------------------------------------
# Provider: Local CSV fallback
# ---------------------------------------------------------------------------

def _search_local_csv(query: str) -> List[Dict]:
    """Fallback: search a static CSV file bundled with the project. Very simple fuzzy match.
    Expected CSV columns: name,calories,proteins,fats,carbohydrates
    """
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'fallback_products.csv')
    if not os.path.isfile(csv_path):
        return []
    results = []
    q = query.lower()
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name', '')
                if q in name.lower():
                    results.append({
                        'name': name[:100],
                        'calories': round(float(row.get('calories', 0)), 1),
                        'proteins': round(float(row.get('proteins', 0)), 1),
                        'fats': round(float(row.get('fats', 0)), 1),
                        'carbohydrates': round(float(row.get('carbohydrates', 0)), 1),
                        '_source': 'local_csv',
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


def search_products(query: str) -> List[Dict]:
    """Query ALL providers in parallel, merge results, rank by relevance, deduplicate.
    Returns the top 30 most relevant matches.
    """
    if not query or len(query.strip()) < 2:
        return []

    query = query.strip()
    all_results: List[Dict] = []

    # Run all providers concurrently
    with ThreadPoolExecutor(max_workers=len(_ALL_PROVIDERS)) as executor:
        futures = {executor.submit(fn, query): fn.__name__ for fn in _ALL_PROVIDERS}
        for future in as_completed(futures):
            try:
                results = future.result(timeout=10)
                if results:
                    all_results.extend(results)
            except Exception:
                pass  # Provider failed — skip silently

    if not all_results:
        return []

    # Score each result by relevance to the query
    scored: List[Tuple[float, Dict]] = []
    for item in all_results:
        score = _relevance_score(query, item.get('name', ''))
        # Small bonus for items that have actual nutrition data
        if item.get('calories', 0) > 0:
            score += 0.05
        scored.append((score, item))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Flatten and deduplicate
    sorted_items = [item for _, item in scored]
    deduped = _deduplicate(sorted_items)

    # Remove internal _source key before returning
    for item in deduped:
        item.pop('_source', None)

    return deduped[:30]
