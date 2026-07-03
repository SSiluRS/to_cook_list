<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Culinary Recipes
        </h1>
        <p class="text-slate-400 text-sm mt-1">Browse public recipes, schedule meals, and see what you can cook from your pantry stock.</p>
      </div>

      <button 
        @click="openCreateDialog" 
        class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7-7H5" />
        </svg>
        Create Recipe
      </button>
    </div>

    <!-- Filters Row -->
    <div class="flex items-center gap-3 border-b border-slate-800/40 pb-4">
      <button 
        v-for="filter in ['All', 'My', 'Shared', 'Public']" 
        :key="filter"
        @click="activeFilter = filter"
        class="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition border"
        :class="activeFilter === filter 
          ? 'bg-slate-800 border-slate-700 text-brand-400 font-bold' 
          : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'"
      >
        {{ filter }} Recipes
      </button>
    </div>

    <!-- Alert Banner -->
    <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <!-- Recipes Grid -->
    <div v-if="loading" class="py-12 flex justify-center">
      <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
    </div>

    <div v-else-if="filteredRecipes.length === 0" class="py-16 text-center text-slate-500 border border-dashed border-slate-800 rounded-2xl">
      <p class="text-base font-semibold text-slate-400">No recipes found</p>
      <p class="text-sm text-slate-500 mt-1">Try creating one or selecting a different filter.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div 
        v-for="recipe in filteredRecipes" 
        :key="recipe.id"
        class="rounded-2xl glass-card p-6 flex flex-col justify-between hover:shadow-xl hover:shadow-brand-950/5 relative overflow-hidden"
      >
        <!-- Top row: visibility and matching -->
        <div class="flex justify-between items-start mb-4">
          <span 
            class="text-[10px] uppercase font-bold tracking-wider px-2 py-1 rounded bg-slate-900 border border-slate-800"
            :class="recipe.is_public ? 'text-emerald-400' : 'text-amber-400'"
          >
            {{ recipe.is_public ? 'Public' : 'Private' }}
          </span>

          <!-- Smart Match badge -->
          <span 
            v-if="recipe.smart_match"
            class="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded border"
            :class="recipe.smart_match.can_cook 
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
              : 'bg-slate-900 text-slate-400 border-slate-800'"
          >
            {{ recipe.smart_match.can_cook ? 'Ready' : `Match: ${recipe.smart_match.match_percentage}%` }}
          </span>
        </div>

        <!-- Recipe Content -->
        <div class="space-y-2 mb-6">
          <router-link :to="`/recipes/${recipe.id}`">
            <h3 class="font-extrabold text-lg text-slate-100 hover:text-brand-400 transition line-clamp-1">
              {{ recipe.title }}
            </h3>
          </router-link>
          
          <p class="text-xs text-slate-500 font-semibold">
            By <span class="text-slate-400">@{{ recipe.author_username || 'anonymous' }}</span>
          </p>
          
          <p class="text-slate-400 text-sm line-clamp-2 leading-relaxed">
            {{ recipe.description || 'No description available.' }}
          </p>
        </div>

        <!-- Recipe KBJU summary row -->
        <div v-if="recipe.total_kbju" class="border-t border-slate-800/40 pt-4 flex justify-between items-center text-xs">
          <div class="text-slate-400 font-bold">
            {{ Math.round(recipe.total_kbju.calories) }} <span class="text-[10px] text-slate-500 uppercase">kcal</span>
          </div>
          <div class="flex gap-2.5 text-slate-500 font-medium">
            <span>P: <strong class="text-emerald-400 font-medium">{{ recipe.total_kbju.proteins }}g</strong></span>
            <span>F: <strong class="text-amber-400 font-medium">{{ recipe.total_kbju.fats }}g</strong></span>
            <span>C: <strong class="text-indigo-400 font-medium">{{ recipe.total_kbju.carbohydrates }}g</strong></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Recipe Dialog -->
    <div v-if="showCreateDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 overflow-y-auto">
      <div class="w-full max-w-2xl p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative my-8">
        <h3 class="text-xl font-bold text-slate-100 mb-5">Create Custom Recipe</h3>
        
        <form @submit.prevent="saveRecipe" class="space-y-5">
          <!-- Text fields -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Recipe Title</label>
              <input 
                v-model="newRecipe.title" 
                type="text" 
                required 
                placeholder="e.g. Avocado Toast"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm font-semibold"
              />
            </div>
            
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Short Description</label>
              <input 
                v-model="newRecipe.description" 
                type="text" 
                placeholder="e.g. Simple healthy breakfast option"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Cooking Instructions</label>
            <textarea 
              v-model="newRecipe.instruction" 
              rows="3"
              placeholder="e.g. 1. Toast bread. 2. Mash avocado and spread..."
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            ></textarea>
          </div>

          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Visibility</span>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="newRecipe.is_public" class="sr-only peer">
              <div class="w-11 h-6 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-slate-300 after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-500 peer-checked:after:bg-white"></div>
              <span class="ml-3 text-sm font-medium text-slate-300">{{ newRecipe.is_public ? 'Public' : 'Private' }}</span>
            </label>
          </div>

          <!-- Dynamic Ingredients List -->
          <div class="border-t border-slate-800/40 pt-4">
            <div class="flex justify-between items-center mb-3">
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Ingredients</span>
              <button 
                type="button" 
                @click="addIngredientRow"
                class="text-xs text-brand-400 hover:text-brand-300 font-bold flex items-center gap-1"
              >
                + Add Ingredient
              </button>
            </div>

            <div class="space-y-2.5 max-h-48 overflow-y-auto pr-2">
              <div 
                v-for="(ing, idx) in newRecipe.ingredients" 
                :key="idx"
                class="flex gap-3 items-center"
              >
                <!-- Product select -->
                <select 
                  v-model="ing.product_id" 
                  required
                  class="flex-1 px-3 py-2 rounded-xl glass-input text-xs font-semibold"
                >
                  <option value="" disabled>-- Select Ingredient --</option>
                  <option 
                    v-for="prod in products" 
                    :key="prod.id" 
                    :value="prod.id"
                  >
                    {{ prod.name }} ({{ prod.calories }} kcal/100g)
                  </option>
                </select>

                <!-- Weight input -->
                <input 
                  v-model.number="ing.weight_g" 
                  type="number" 
                  required
                  min="1"
                  placeholder="Weight (g)"
                  class="w-28 px-3 py-2 rounded-xl glass-input text-xs font-semibold text-center"
                />

                <!-- Remove row button -->
                <button 
                  type="button" 
                  @click="removeIngredientRow(idx)"
                  class="p-2 rounded bg-slate-900 text-slate-500 hover:text-rose-400 border border-slate-800 transition"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Live KBJU calculation preview -->
          <div class="p-4 rounded-xl bg-slate-900/30 border border-slate-850 flex justify-between items-center text-xs">
            <span class="font-bold text-slate-400 uppercase tracking-wider">Live Preview (KBJU):</span>
            <div class="flex gap-4 font-semibold text-slate-300">
              <span>Calories: <strong class="text-slate-100">{{ liveKbju.calories }}</strong> kcal</span>
              <span>P: <strong class="text-emerald-400">{{ liveKbju.proteins }}g</strong></span>
              <span>F: <strong class="text-amber-400">{{ liveKbju.fats }}g</strong></span>
              <span>C: <strong class="text-indigo-400">{{ liveKbju.carbohydrates }}g</strong></span>
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="closeCreateDialog"
              class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 text-sm font-semibold transition"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold shadow-lg shadow-brand-800/25"
            >
              Save Recipe
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const loading = ref(true)
const recipes = ref([])
const products = ref([])
const activeFilter = ref('All')
const error = ref(null)

const showCreateDialog = ref(false)
const newRecipe = ref({
  title: '',
  description: '',
  instruction: '',
  is_public: true,
  ingredients: []
})

// Filter recipes according to activeFilter
const filteredRecipes = computed(() => {
  if (activeFilter.value === 'All') return recipes.value
  if (activeFilter.value === 'My') return recipes.value.filter(r => r.author_id === authStore.token ? true : r.author_username === authStore.username)
  if (activeFilter.value === 'Shared') return recipes.value.filter(r => r.author_username !== authStore.username && !r.is_public)
  if (activeFilter.value === 'Public') return recipes.value.filter(r => r.is_public)
  return recipes.value
})

// Live KBJU calculations of the recipe in the creation form
const liveKbju = computed(() => {
  let calories = 0
  let proteins = 0
  let fats = 0
  let carbohydrates = 0
  
  newRecipe.value.ingredients.forEach(ing => {
    if (!ing.product_id || !ing.weight_g) return
    const prod = products.value.find(p => p.id === ing.product_id)
    if (!prod) return
    
    calories += (ing.weight_g * (prod.calories || 0)) / 100
    proteins += (ing.weight_g * (prod.proteins || 0)) / 100
    fats += (ing.weight_g * (prod.fats || 0)) / 100
    carbohydrates += (ing.weight_g * (prod.carbohydrates || 0)) / 100
  })
  
  return {
    calories: Math.round(calories * 10) / 10,
    proteins: Math.round(proteins * 10) / 10,
    fats: Math.round(fats * 10) / 10,
    carbohydrates: Math.round(carbohydrates * 10) / 10
  }
})

const loadRecipes = async () => {
  loading.value = true
  try {
    const recipesRes = await api.get('/api/v1/recipes/')
    recipes.value = recipesRes.data

    const productsRes = await api.get('/api/v1/products/')
    products.value = productsRes.data
  } catch (err) {
    error.value = 'Failed to load recipes data'
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  showCreateDialog.value = true
  newRecipe.value = {
    title: '',
    description: '',
    instruction: '',
    is_public: true,
    ingredients: [{ product_id: '', weight_g: null }]
  }
}

const addIngredientRow = () => {
  newRecipe.value.ingredients.push({ product_id: '', weight_g: null })
}

const removeIngredientRow = (idx) => {
  newRecipe.value.ingredients.splice(idx, 1)
}

const saveRecipe = async () => {
  // Validate ingredients are not empty
  const validIngredients = newRecipe.value.ingredients.filter(i => i.product_id && i.weight_g > 0)
  if (validIngredients.length === 0) {
    error.value = 'You must add at least one valid ingredient with weight.'
    return
  }
  
  try {
    const payload = {
      ...newRecipe.value,
      ingredients: validIngredients
    }
    const response = await api.post('/api/v1/recipes/', payload)
    recipes.value.push(response.data)
    closeCreateDialog()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save recipe'
  }
}

const closeCreateDialog = () => {
  showCreateDialog.value = false
  newRecipe.value = {
    title: '',
    description: '',
    instruction: '',
    is_public: true,
    ingredients: []
  }
}

onMounted(() => {
  loadRecipes()
})
</script>
