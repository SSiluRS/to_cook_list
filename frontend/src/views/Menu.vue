<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Menu Planner
        </h1>
        <p class="text-slate-400 text-sm mt-1">Plan your daily breakfasts, lunches, dinners, and snacks for the week.</p>
      </div>

      <!-- Add to menu button -->
      <button 
        @click="openAddDialog(new Date())" 
        class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7-7H5" />
        </svg>
        Schedule Meal
      </button>
    </div>

    <!-- Alert Banner -->
    <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <!-- Calendar view: 7 Days horizontal/vertical layout -->
    <div v-if="loading" class="py-12 flex justify-center">
      <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
    </div>

    <div v-else class="space-y-6">
      <div 
        v-for="day in weekDays" 
        :key="day.dateStr"
        class="p-6 rounded-2xl glass-panel flex flex-col md:flex-row md:items-start justify-between gap-6 border border-slate-800/40 relative overflow-hidden"
      >
        <!-- Date display -->
        <div class="w-full md:w-48 shrink-0">
          <h3 class="text-base font-bold text-slate-100">{{ day.dayName }}</h3>
          <p class="text-xs text-brand-400 font-semibold mt-0.5">{{ day.dateFormatted }}</p>
          <button 
            @click="openAddDialog(day.date)"
            class="text-[10px] text-slate-500 hover:text-brand-400 font-bold uppercase tracking-wider mt-3 flex items-center gap-1"
          >
            + Add to this day
          </button>
        </div>

        <!-- Meals list for this day -->
        <div class="flex-1 space-y-3">
          <div v-if="day.meals.length === 0" class="text-slate-600 text-xs py-4 italic font-medium">
            No meals planned for this day.
          </div>
          
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div 
              v-for="meal in day.meals" 
              :key="meal.id"
              class="p-3.5 rounded-xl glass-card flex items-center justify-between gap-3 border border-slate-800/40"
            >
              <div class="truncate">
                <div class="flex items-center gap-2">
                  <span 
                    class="text-[9px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded border"
                    :class="{
                      'bg-amber-500/10 text-amber-400 border-amber-500/20': meal.meal_type === 'Breakfast',
                      'bg-emerald-500/10 text-emerald-400 border-emerald-500/20': meal.meal_type === 'Lunch',
                      'bg-indigo-500/10 text-indigo-400 border-indigo-500/20': meal.meal_type === 'Dinner',
                      'bg-pink-500/10 text-pink-400 border-pink-500/20': meal.meal_type === 'Snack',
                    }"
                  >
                    {{ meal.meal_type }}
                  </span>
                  
                  <span 
                    v-if="meal.recipe && meal.recipe.smart_match"
                    class="text-[8px] uppercase font-bold tracking-wider px-1 rounded border"
                    :class="meal.recipe.smart_match.can_cook 
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/15' 
                      : 'bg-rose-500/10 text-rose-400 border-rose-500/15'"
                  >
                    {{ meal.recipe.smart_match.can_cook ? 'Ready' : 'Missing' }}
                  </span>
                </div>

                <h4 class="font-bold text-slate-200 text-sm mt-2 hover:text-brand-400 transition truncate">
                  <router-link :to="`/recipes/${meal.recipe_id}`">{{ meal.recipe_title }}</router-link>
                </h4>
              </div>

              <!-- Delete button -->
              <button 
                @click="removeMeal(meal.id)"
                class="p-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-500 hover:text-rose-400 transition"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Meal Dialog -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-sm p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Schedule Meal</h3>
        
        <form @submit.prevent="addMeal" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Date</label>
            <input v-model="addForm.date" type="date" required class="w-full px-4 py-3 rounded-xl glass-input text-sm" />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Meal Type</label>
            <select v-model="addForm.meal_type" required class="w-full px-4 py-3 rounded-xl glass-input text-sm">
              <option value="Breakfast">Breakfast</option>
              <option value="Lunch">Lunch</option>
              <option value="Dinner">Dinner</option>
              <option value="Snack">Snack</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Select Recipe</label>
            <select v-model="addForm.recipe_id" required class="w-full px-4 py-3 rounded-xl glass-input text-sm">
              <option value="" disabled>-- Select Recipe --</option>
              <option 
                v-for="rec in recipes" 
                :key="rec.id" 
                :value="rec.id"
              >
                {{ rec.title }}
              </option>
            </select>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="showAddDialog = false" class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 text-sm font-semibold transition">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold">Schedule</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const loading = ref(true)
const menuItems = ref([])
const recipes = ref([])
const error = ref(null)

const showAddDialog = ref(false)
const addForm = ref({ date: '', meal_type: 'Breakfast', recipe_id: '' })

// Generate next 7 days list starting from today
const weekDays = ref([])

const loadMenu = async () => {
  loading.value = true
  try {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const endOfWeek = new Date(today)
    endOfWeek.setDate(endOfWeek.getDate() + 7)

    const menuRes = await api.get(`/api/v1/menu/?start_date=${today.toISOString()}&end_date=${endOfWeek.toISOString()}`)
    menuItems.value = menuRes.data

    const recipesRes = await api.get('/api/v1/recipes/')
    recipes.value = recipesRes.data

    // Build the 7 days array
    const days = []
    for (let i = 0; i < 7; i++) {
      const date = new Date(today)
      date.setDate(today.getDate() + i)
      
      const dateStr = date.toISOString().split('T')[0]
      
      const dayMeals = menuItems.value.filter(item => {
        const itemDateStr = new Date(item.date).toISOString().split('T')[0]
        return itemDateStr === dateStr
      })

      days.push({
        date,
        dateStr,
        dayName: date.toLocaleDateString('en-US', { weekday: 'long' }),
        dateFormatted: date.toLocaleDateString('en-US', { day: 'numeric', month: 'short' }),
        meals: dayMeals
      })
    }
    
    weekDays.value = days
  } catch (err) {
    error.value = 'Failed to load menu planner'
  } finally {
    loading.value = false
  }
}

const openAddDialog = (date) => {
  showAddDialog.value = true
  // Format date to yyyy-mm-dd
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  addForm.value = {
    date: `${year}-${month}-${day}`,
    meal_type: 'Breakfast',
    recipe_id: ''
  }
}

const addMeal = async () => {
  try {
    const datetimeStr = new Date(addForm.value.date).toISOString()
    await api.post('/api/v1/menu/', {
      date: datetimeStr,
      meal_type: addForm.value.meal_type,
      recipe_id: addForm.value.recipe_id
    })
    showAddDialog.value = false
    await loadMenu()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to schedule meal')
  }
}

const removeMeal = async (id) => {
  try {
    await api.delete(`/api/v1/menu/${id}`)
    await loadMenu()
  } catch (err) {
    error.value = 'Failed to delete menu item'
  }
}

onMounted(() => {
  loadMenu()
})
</script>
