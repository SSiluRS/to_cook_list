<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Pantry Stock
        </h1>
        <p class="text-slate-400 text-sm mt-1">Manage the ingredients you have available in your kitchen.</p>
      </div>
      
      <!-- Quick Add Toggle -->
      <button 
        @click="showAddDialog = true" 
        class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7-7H5" />
        </svg>
        Add Ingredient
      </button>
    </div>

    <!-- Alert Banner -->
    <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <!-- Main Pantry Table / List -->
    <div class="glass-panel rounded-2xl overflow-hidden">
      <div v-if="loading" class="py-12 flex justify-center">
        <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
      </div>

      <div v-else-if="pantryItems.length === 0" class="py-16 text-center text-slate-500">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 mx-auto text-slate-600 mb-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
        </svg>
        <p class="text-base font-semibold text-slate-400">Your pantry is empty</p>
        <p class="text-sm text-slate-500 mt-1">Add ingredients to calculate what recipes you can cook.</p>
        <button @click="showAddDialog = true" class="mt-4 px-4 py-2 rounded-xl border border-slate-800 bg-slate-900/40 text-brand-400 hover:text-brand-300 text-xs font-semibold">
          Add your first ingredient
        </button>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-800/60 bg-slate-900/20 text-xs uppercase tracking-wider font-semibold text-slate-400">
              <th class="p-4 pl-6">Ingredient Name</th>
              <th class="p-4">Calories (100g)</th>
              <th class="p-4">P / F / C (100g)</th>
              <th class="p-4 text-center">Available Stock</th>
              <th class="p-4 pr-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/40 text-sm text-slate-300">
            <tr 
              v-for="item in pantryItems" 
              :key="item.id" 
              class="hover:bg-slate-900/20 transition-colors"
            >
              <td class="p-4 pl-6 font-bold text-slate-200">
                {{ item.product?.name || 'Unknown product' }}
              </td>
              <td class="p-4">
                {{ item.product?.calories || 0 }} kcal
              </td>
              <td class="p-4">
                <span class="text-emerald-400 font-medium">P: {{ item.product?.proteins }}g</span> / 
                <span class="text-amber-400 font-medium">F: {{ item.product?.fats }}g</span> / 
                <span class="text-indigo-400 font-medium">C: {{ item.product?.carbohydrates }}g</span>
              </td>
              <td class="p-4">
                <div class="flex items-center justify-center gap-2">
                  <!-- Quick adjust weight buttons -->
                  <button @click="adjustWeight(item, -100)" class="w-7 h-7 rounded bg-slate-800 hover:bg-slate-700 font-bold text-slate-300 text-xs transition">-</button>
                  
                  <input 
                    type="number" 
                    v-model.number="item.weight_g" 
                    @change="updateWeight(item)"
                    class="w-20 px-2 py-1 text-center rounded bg-slate-950 border border-slate-800 text-xs font-semibold text-white focus:outline-none focus:border-brand-500"
                  />
                  <span class="text-xs text-slate-500 font-semibold">g</span>
                  
                  <button @click="adjustWeight(item, 100)" class="w-7 h-7 rounded bg-slate-800 hover:bg-slate-700 font-bold text-slate-300 text-xs transition">+</button>
                </div>
              </td>
              <td class="p-4 pr-6 text-right">
                <button 
                  @click="deleteItem(item.product_id)"
                  class="p-2 rounded-lg border border-slate-800 hover:border-rose-950 text-slate-500 hover:text-rose-400 hover:bg-rose-950/15 transition-colors"
                  title="Remove from pantry"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Ingredient Modal Dialog -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Add Ingredient to Pantry</h3>
        
        <form @submit.prevent="addIngredient" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Select Product</label>
            <select 
              v-model="newProduct.product_id" 
              required
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            >
              <option value="" disabled>-- Choose a product from catalog --</option>
              <option 
                v-for="prod in availableProducts" 
                :key="prod.id" 
                :value="prod.id"
              >
                {{ prod.name }} ({{ prod.calories }} kcal/100g)
              </option>
            </select>
            <p class="text-xs text-slate-500 mt-2 font-medium">
              Can't find your product? 
              <router-link to="/products" class="text-brand-400 hover:text-brand-300 font-semibold underline">Create new product &rarr;</router-link>
            </p>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Weight (grams)</label>
            <input 
              v-model.number="newProduct.weight_g" 
              type="number" 
              required 
              min="1"
              placeholder="e.g. 500"
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            />
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
              Add Stock
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
const pantryItems = ref([])
const allProducts = ref([])
const error = ref(null)

const showAddDialog = ref(false)
const newProduct = ref({
  product_id: '',
  weight_g: null
})

// Compute list of products that are NOT already in the user's pantry
const availableProducts = computed(() => {
  const pantryProductIds = pantryItems.value.map(item => item.product_id)
  return allProducts.value.filter(prod => !pantryProductIds.includes(prod.id))
})

const loadPantry = async () => {
  loading.value = true
  try {
    const pantryRes = await api.get('/api/v1/pantry/')
    pantryItems.value = pantryRes.data

    const productsRes = await api.get('/api/v1/products/')
    allProducts.value = productsRes.data
  } catch (err) {
    error.value = 'Failed to load pantry data'
  } finally {
    loading.value = false
  }
}

const adjustWeight = async (item, delta) => {
  const newWeight = Math.max(0, item.weight_g + delta)
  if (newWeight === 0) {
    await deleteItem(item.product_id)
  } else {
    item.weight_g = newWeight
    await updateWeight(item)
  }
}

const updateWeight = async (item) => {
  if (item.weight_g <= 0) {
    await deleteItem(item.product_id)
    return
  }
  try {
    const response = await api.put('/api/v1/pantry/', {
      product_id: item.product_id,
      weight_g: item.weight_g
    })
    // Update local list
    const index = pantryItems.value.findIndex(i => i.product_id === item.product_id)
    if (index !== -1) {
      pantryItems.value[index] = response.data
    }
  } catch (err) {
    error.value = 'Failed to update ingredient weight'
  }
}

const deleteItem = async (productId) => {
  try {
    await api.delete(`/api/v1/pantry/${productId}`)
    pantryItems.value = pantryItems.value.filter(i => i.product_id !== productId)
  } catch (err) {
    error.value = 'Failed to delete ingredient'
  }
}

const addIngredient = async () => {
  try {
    const response = await api.put('/api/v1/pantry/', {
      product_id: newProduct.value.product_id,
      weight_g: newProduct.value.weight_g
    })
    
    // Find the product details in allProducts to attach it locally
    const product = allProducts.value.find(p => p.id === newProduct.value.product_id)
    const addedItem = { ...response.data, product }
    
    pantryItems.value.push(addedItem)
    closeAddDialog()
  } catch (err) {
    error.value = 'Failed to add ingredient'
  }
}

const closeAddDialog = () => {
  showAddDialog.value = false
  newProduct.value = { product_id: '', weight_g: null }
}

onMounted(() => {
  loadPantry()
})
</script>
