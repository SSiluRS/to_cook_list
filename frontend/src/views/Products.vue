<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          KBJU Catalog
        </h1>
        <p class="text-slate-400 text-sm mt-1">Browse food nutritional compositions (per 100g) or add custom ingredients.</p>
      </div>

      <button 
        @click="showAddDialog = true" 
        class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7-7H5" />
        </svg>
        New Product
      </button>
    </div>

    <!-- Filter and Search Row -->
    <div class="flex items-center gap-4 max-w-md">
      <div class="relative flex-1">
        <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>
        </span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search products..."
          class="w-full pl-10 pr-4 py-2.5 rounded-xl glass-input text-xs font-semibold"
        />
      </div>
    </div>

    <!-- Alert Banner -->
    <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <!-- Products List -->
    <div class="glass-panel rounded-2xl overflow-hidden">
      <div v-if="loading" class="py-12 flex justify-center">
        <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
      </div>

      <div v-else-if="filteredProducts.length === 0" class="py-16 text-center text-slate-500">
        <p class="text-base font-semibold text-slate-400">No products found</p>
        <p class="text-sm text-slate-500 mt-1">Try adjusting your search query or add a custom product.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-800/60 bg-slate-900/20 text-xs uppercase tracking-wider font-semibold text-slate-400">
              <th class="p-4 pl-6">Product Name</th>
              <th class="p-4">Calories (100g)</th>
              <th class="p-4">Proteins (100g)</th>
              <th class="p-4">Fats (100g)</th>
              <th class="p-4 pr-6">Carbohydrates (100g)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/40 text-sm text-slate-300">
            <tr 
              v-for="prod in filteredProducts" 
              :key="prod.id"
              class="hover:bg-slate-900/20 transition-colors"
            >
              <td class="p-4 pl-6 font-bold text-slate-200">{{ prod.name }}</td>
              <td class="p-4 font-medium">{{ prod.calories }} kcal</td>
              <td class="p-4 text-emerald-400 font-semibold">{{ prod.proteins }}g</td>
              <td class="p-4 text-amber-400 font-semibold">{{ prod.fats }}g</td>
              <td class="p-4 pr-6 text-indigo-400 font-semibold">{{ prod.carbohydrates }}g</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Product Modal -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Create New Product</h3>
        
        <form @submit.prevent="createProduct" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Product Name</label>
            <input 
              v-model="newProduct.name" 
              type="text" 
              required 
              placeholder="e.g. Avocado"
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Calories (kcal)</label>
              <input 
                v-model.number="newProduct.calories" 
                type="number" 
                step="0.1"
                required 
                placeholder="160"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Proteins (g)</label>
              <input 
                v-model.number="newProduct.proteins" 
                type="number" 
                step="0.1"
                required 
                placeholder="2"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Fats (g)</label>
              <input 
                v-model.number="newProduct.fats" 
                type="number" 
                step="0.1"
                required 
                placeholder="15"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Carbs (g)</label>
              <input 
                v-model.number="newProduct.carbohydrates" 
                type="number" 
                step="0.1"
                required 
                placeholder="8"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="closeAddDialog"
              class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 text-sm font-semibold transition"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold shadow-lg shadow-brand-800/25"
            >
              Save Product
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

const loading = ref(true)
const products = ref([])
const searchQuery = ref('')
const error = ref(null)

const showAddDialog = ref(false)
const newProduct = ref({
  name: '',
  calories: null,
  proteins: null,
  fats: null,
  carbohydrates: null,
  is_public: true
})

const filteredProducts = computed(() => {
  if (!searchQuery.value.trim()) return products.value
  const query = searchQuery.value.toLowerCase()
  return products.value.filter(p => p.name.toLowerCase().includes(query))
})

const loadProducts = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/v1/products/')
    products.value = res.data
  } catch (err) {
    error.value = 'Failed to load catalog products'
  } finally {
    loading.value = false
  }
}

const createProduct = async () => {
  try {
    const res = await api.post('/api/v1/products/', newProduct.value)
    products.value.push(res.data)
    closeAddDialog()
  } catch (err) {
    error.value = 'Failed to create product. Make sure the name is unique.'
  }
}

const closeAddDialog = () => {
  showAddDialog.value = false
  newProduct.value = {
    name: '',
    calories: null,
    proteins: null,
    fats: null,
    carbohydrates: null,
    is_public: true
  }
}

onMounted(() => {
  loadProducts()
})
</script>
