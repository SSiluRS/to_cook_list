<template>
  <div class="space-y-8">
    <!-- Back Button -->
    <div>
      <router-link to="/recipes" class="text-xs font-semibold text-slate-400 hover:text-brand-400 transition flex items-center gap-1">
        &larr; Back to Recipes Catalog
      </router-link>
    </div>

    <div v-if="loading" class="py-12 flex justify-center">
      <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
    </div>

    <!-- Error Banner -->
    <div v-else-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <!-- Main Content -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left 2 Cols: Details, Instructions, Matching -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Title Panel -->
        <div class="p-6 rounded-2xl glass-panel relative overflow-hidden">
          <div class="absolute -top-16 -left-16 w-32 h-32 bg-brand-500/5 rounded-full blur-3xl"></div>
          
          <div class="flex justify-between items-start mb-4">
            <span class="text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800">
              {{ recipe.is_public ? 'Public' : 'Private' }}
            </span>
            <div class="text-xs text-slate-500 font-semibold">
              Recipe by <span class="text-slate-300">@{{ recipe.author_username || 'anonymous' }}</span>
            </div>
          </div>
          
          <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
            {{ recipe.title }}
          </h1>
          <p class="text-slate-400 text-sm mt-2 leading-relaxed">
            {{ recipe.description || 'No description provided.' }}
          </p>
        </div>

        <!-- Instructions Panel -->
        <div class="p-6 rounded-2xl glass-panel">
          <h3 class="text-base font-bold text-slate-200 mb-3 uppercase tracking-wider text-xs">Cooking Instructions</h3>
          <p class="text-slate-300 text-sm whitespace-pre-line leading-relaxed">
            {{ recipe.instruction || 'No instructions provided.' }}
          </p>
        </div>

        <!-- Smart Matching / Ingredients Stock Check -->
        <div class="p-6 rounded-2xl glass-panel">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-base font-bold text-slate-200 uppercase tracking-wider text-xs">Pantry Ingredients Match</h3>
            <span 
              v-if="recipe.smart_match"
              class="px-3 py-1.5 rounded-xl text-xs font-bold uppercase tracking-wider border"
              :class="recipe.smart_match.can_cook 
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                : 'bg-rose-500/10 text-rose-400 border-rose-500/20'"
            >
              {{ recipe.smart_match.can_cook ? 'Fully Stocked' : `Stock: ${recipe.smart_match.match_percentage}%` }}
            </span>
          </div>

          <!-- Matching List -->
          <div v-if="recipe.smart_match" class="space-y-3">
            <div 
              v-for="ing in recipe.smart_match.ingredients" 
              :key="ing.product_id"
              class="p-4 rounded-xl flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border"
              :class="ing.is_sufficient 
                ? 'bg-emerald-500/5 border-emerald-500/10 text-emerald-300' 
                : 'bg-rose-500/5 border-rose-500/10 text-rose-300'"
            >
              <div>
                <h4 class="font-bold text-sm text-slate-200">{{ ing.product_name }}</h4>
                <p class="text-xs text-slate-500 mt-0.5">
                  Required: <span class="text-slate-400 font-semibold">{{ ing.required_weight_g }}g</span>
                </p>
              </div>

              <div class="flex items-center gap-4 text-xs font-medium">
                <div>
                  Available: 
                  <span class="font-bold" :class="ing.is_sufficient ? 'text-emerald-400' : 'text-slate-400'">
                    {{ ing.available_weight_g }}g
                  </span>
                </div>
                
                <div v-if="!ing.is_sufficient" class="px-2.5 py-1 rounded bg-rose-950/20 text-rose-400 border border-rose-500/20">
                  Missing {{ ing.missing_weight_g }}g
                </div>
                <div v-else class="px-2.5 py-1 rounded bg-emerald-950/20 text-emerald-400 border border-emerald-500/20">
                  In Stock
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right 1 Col: Nutrition details, Action board -->
      <div class="space-y-6">
        <!-- Nutrition Details (KBJU) -->
        <div v-if="recipe.total_kbju" class="p-6 rounded-2xl glass-panel space-y-5">
          <h3 class="text-base font-bold text-slate-200 uppercase tracking-wider text-xs">Nutritional Info</h3>
          
          <!-- Tabs: Total vs Per 100g -->
          <div class="flex gap-2 p-1 bg-slate-950 border border-slate-900 rounded-xl">
            <button 
              @click="nutritionTab = 'total'" 
              class="flex-1 py-1.5 rounded-lg text-xs font-bold transition"
              :class="nutritionTab === 'total' ? 'bg-slate-800 text-brand-400' : 'text-slate-500'"
            >
              Total Recipe
            </button>
            <button 
              @click="nutritionTab = 'per100g'" 
              class="flex-1 py-1.5 rounded-lg text-xs font-bold transition"
              :class="nutritionTab === 'per100g' ? 'bg-slate-800 text-brand-400' : 'text-slate-500'"
            >
              Per 100g
            </button>
          </div>

          <!-- Active nutrition KBJU mapping -->
          <div class="space-y-4">
            <div class="flex justify-between items-center text-sm font-semibold border-b border-slate-850 pb-2">
              <span class="text-slate-400">Calories</span>
              <span class="text-slate-100 font-bold text-base">{{ activeKbju.calories }} kcal</span>
            </div>
            <div class="flex justify-between items-center text-sm font-semibold border-b border-slate-850 pb-2">
              <span class="text-slate-400">Proteins</span>
              <span class="text-emerald-400">{{ activeKbju.proteins }}g</span>
            </div>
            <div class="flex justify-between items-center text-sm font-semibold border-b border-slate-850 pb-2">
              <span class="text-slate-400">Fats</span>
              <span class="text-amber-400">{{ activeKbju.fats }}g</span>
            </div>
            <div class="flex justify-between items-center text-sm font-semibold border-b border-slate-850 pb-2">
              <span class="text-slate-400">Carbohydrates</span>
              <span class="text-indigo-400">{{ activeKbju.carbohydrates }}g</span>
            </div>
          </div>
        </div>

        <!-- Action Board -->
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-base font-bold text-slate-200 uppercase tracking-wider text-xs">Action Board</h3>
          
          <button @click="showScheduleDialog = true" class="w-full py-3 rounded-xl gradient-btn text-white text-sm font-bold shadow-lg shadow-brand-800/25 flex items-center justify-center gap-2">
            Schedule to Menu
          </button>

          <button @click="showShareDialog = true" class="w-full py-3 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-900/40 text-slate-300 hover:text-white transition text-sm font-bold flex items-center justify-center gap-2">
            Share Recipe Access
          </button>

          <button @click="showRequestDialog = true" class="w-full py-3 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-900/40 text-slate-300 hover:text-white transition text-sm font-bold flex items-center justify-center gap-2">
            Request "Cook for Me"
          </button>

          <button 
            v-if="isOwner"
            @click="deleteRecipe" 
            class="w-full py-3 rounded-xl border border-rose-950/20 bg-rose-950/10 hover:bg-rose-950/20 text-rose-400 transition text-sm font-bold flex items-center justify-center gap-2"
          >
            Delete Recipe Card
          </button>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Schedule Modal -->
    <div v-if="showScheduleDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-sm p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Schedule to Menu</h3>
        
        <form @submit.prevent="scheduleRecipe" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Select Date</label>
            <input v-model="scheduleForm.date" type="date" required class="w-full px-4 py-3 rounded-xl glass-input text-sm" />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Meal Type</label>
            <select v-model="scheduleForm.meal_type" required class="w-full px-4 py-3 rounded-xl glass-input text-sm">
              <option value="Breakfast">Breakfast</option>
              <option value="Lunch">Lunch</option>
              <option value="Dinner">Dinner</option>
              <option value="Snack">Snack</option>
            </select>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="showScheduleDialog = false" class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 text-sm font-semibold transition">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold">Schedule</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Share Modal -->
    <div v-if="showShareDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-sm p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Share Recipe Access</h3>
        
        <form @submit.prevent="shareRecipe" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Target Username or Email</label>
            <input v-model="shareForm.username" type="text" required placeholder="e.g. chef_john" class="w-full px-4 py-3 rounded-xl glass-input text-sm" />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="showShareDialog = false" class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 text-sm font-semibold transition">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold">Share</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Request Modal -->
    <div v-if="showRequestDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-sm p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Request Cooking ("Cook for Me")</h3>
        
        <form @submit.prevent="sendRequest" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Cook Username or Email</label>
            <input v-model="requestForm.username" type="text" required placeholder="e.g. chef_john" class="w-full px-4 py-3 rounded-xl glass-input text-sm" />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="showRequestDialog = false" class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 text-sm font-semibold transition">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold">Send Request</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const recipe = ref({})
const error = ref(null)

const nutritionTab = ref('total')

const showScheduleDialog = ref(false)
const scheduleForm = ref({ date: '', meal_type: 'Breakfast' })

const showShareDialog = ref(false)
const shareForm = ref({ username: '' })

const showRequestDialog = ref(false)
const requestForm = ref({ username: '' })

const isOwner = computed(() => {
  return recipe.value.author_username === authStore.username
})

const activeKbju = computed(() => {
  if (nutritionTab.value === 'total') return recipe.value.total_kbju || {}
  return recipe.value.kbju_per_100g || {}
})

const loadRecipe = async () => {
  loading.value = true
  try {
    const res = await api.get(`/api/v1/recipes/${route.params.id}`)
    recipe.value = res.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load recipe details'
  } finally {
    loading.value = false
  }
}

const deleteRecipe = async () => {
  if (!confirm('Are you sure you want to delete this recipe?')) return
  try {
    await api.delete(`/api/v1/recipes/${route.params.id}`)
    router.push('/recipes')
  } catch (err) {
    error.value = 'Failed to delete recipe'
  }
}

const scheduleRecipe = async () => {
  try {
    // Backend expects DateTime (ISO format)
    const datetimeStr = new Date(scheduleForm.value.date).toISOString()
    await api.post('/api/v1/menu/', {
      date: datetimeStr,
      meal_type: scheduleForm.value.meal_type,
      recipe_id: route.params.id
    })
    showScheduleDialog.value = false
    alert('Recipe scheduled successfully!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to schedule recipe')
  }
}

const shareRecipe = async () => {
  try {
    await api.post('/api/v1/shares/', {
      shared_with_username: shareForm.value.username,
      recipe_id: route.params.id
    })
    showShareDialog.value = false
    alert('Recipe shared successfully!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to share recipe')
  }
}

const sendRequest = async () => {
  try {
    await api.post('/api/v1/cooking-requests/', {
      receiver_username: requestForm.value.username,
      recipe_id: route.params.id
    })
    showRequestDialog.value = false
    alert('Cooking request sent successfully!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to send cooking request')
  }
}

onMounted(() => {
  loadRecipe()
})
</script>
