<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Планировщик меню
        </h1>
        <p class="text-slate-400 text-sm mt-1">Планируйте свои ежедневные завтраки, обеды, ужины и перекусы на неделю вперед.</p>
      </div>

      <!-- Add to menu button -->
      <button 
        @click="openAddDialog(new Date())" 
        class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7-7H5" />
        </svg>
        Запланировать
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
        class="p-6 rounded-2xl glass-panel relative overflow-hidden"
      >
        <!-- Day header info -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-800/40 pb-4 mb-4 gap-2">
          <div>
            <h2 class="font-extrabold text-base text-slate-100 capitalize">
              {{ day.dayName }}
            </h2>
            <p class="text-xs text-slate-500 mt-0.5 font-bold uppercase tracking-wide">
              {{ day.dateFormatted }}
            </p>
          </div>
          
          <button 
            @click="openAddDialog(day.date)"
            class="px-3.5 py-1.5 rounded-lg border border-slate-850 hover:border-slate-800 bg-slate-900/30 hover:bg-slate-850 text-slate-400 hover:text-brand-400 text-xs font-semibold flex items-center justify-center gap-1.5 transition"
          >
            + Добавить блюдо
          </button>
        </div>

        <!-- Meals scheduled for this day -->
        <div v-if="day.meals.length === 0" class="py-6 text-center text-slate-500 text-xs">
          <p>Нет запланированных блюд на этот день.</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <div 
            v-for="meal in day.meals" 
            :key="meal.id"
            class="p-4 rounded-xl glass-card flex flex-col justify-between gap-3 relative border border-slate-850"
          >
            <div>
              <!-- Meal type label -->
              <span 
                class="px-2 py-1 rounded text-[9px] font-bold uppercase tracking-wider block w-max mb-3"
                :class="{
                  'bg-amber-500/10 text-amber-400 border border-amber-500/20': meal.meal_type === 'Breakfast',
                  'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': meal.meal_type === 'Lunch',
                  'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20': meal.meal_type === 'Dinner',
                  'bg-pink-500/10 text-pink-400 border border-pink-500/20': meal.meal_type === 'Snack',
                }"
              >
                {{ translateMealType(meal.meal_type) }}
              </span>

              <h4 class="font-bold text-slate-200 text-sm hover:text-brand-400 transition line-clamp-1">
                <router-link :to="`/recipes/${meal.recipe_id}`">{{ meal.recipe_title }}</router-link>
              </h4>

              <!-- Recipe stats preview -->
              <div v-if="meal.recipe && meal.recipe.total_kbju" class="text-[11px] text-slate-500 font-semibold mt-2.5 space-y-1">
                <p>Калорийность: {{ Math.round(meal.recipe.total_kbju.calories) }} ккал</p>
                <div class="flex gap-2">
                  <span>Б: {{ meal.recipe.total_kbju.proteins }}г</span>
                  <span>Ж: {{ meal.recipe.total_kbju.fats }}г</span>
                  <span>У: {{ meal.recipe.total_kbju.carbohydrates }}г</span>
                </div>
              </div>
            </div>

            <!-- Remove from menu button -->
            <div class="flex justify-between items-center border-t border-slate-900 pt-3">
              <span 
                v-if="meal.recipe && meal.recipe.smart_match"
                class="text-[9px] uppercase font-bold tracking-wider px-2 py-0.5 rounded border"
                :class="meal.recipe.smart_match.can_cook 
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                  : 'bg-slate-950 text-rose-400 border-rose-950/20'"
              >
                {{ meal.recipe.smart_match.can_cook ? 'Готово' : 'Не хватает' }}
              </span>
              
              <button 
                @click="removeMeal(meal.id)"
                class="text-xs text-slate-500 hover:text-rose-400 transition-colors font-medium ml-auto"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Meal Modal -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative animate-scale-in">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Запланировать новое блюдо</h3>
        
        <form @submit.prevent="addMeal" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Выберите дату</label>
            <input 
              v-model="addForm.date" 
              type="date" 
              required 
              class="w-full px-4 py-3 rounded-xl glass-input text-sm font-semibold"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Прием пищи</label>
            <select 
              v-model="addForm.meal_type" 
              required
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            >
              <option value="Breakfast">Завтрак</option>
              <option value="Lunch">Обед</option>
              <option value="Dinner">Ужин</option>
              <option value="Snack">Перекус</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Выберите рецепт</label>
            <select 
              v-model="addForm.recipe_id" 
              required
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            >
              <option value="" disabled>-- Выберите рецепт --</option>
              <option 
                v-for="rec in recipes" 
                :key="rec.id" 
                :value="rec.id"
              >
                {{ rec.title }} ({{ rec.is_public ? 'Публичный' : 'Личный' }})
              </option>
            </select>
            <p class="text-xs text-slate-500 mt-2 font-medium">
              Не нашли нужный рецепт? 
              <router-link to="/recipes" class="text-brand-400 hover:text-brand-300 font-semibold underline">Создать новый рецепт &rarr;</router-link>
            </p>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="showAddDialog = false"
              class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 text-sm font-semibold transition"
            >
              Отмена
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold shadow-lg shadow-brand-800/25"
            >
              Запланировать
            </button>
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
const weekDays = ref([])
const error = ref(null)

const showAddDialog = ref(false)
const addForm = ref({
  date: '',
  meal_type: 'Breakfast',
  recipe_id: ''
})

const translateMealType = (type) => {
  const translations = {
    'Breakfast': 'Завтрак',
    'Lunch': 'Обед',
    'Dinner': 'Ужин',
    'Snack': 'Перекус'
  }
  return translations[type] || type
}

const loadMenu = async () => {
  loading.value = true
  try {
    // Generate dates for the current week starting from today
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    const end = new Date(today)
    end.setDate(end.getDate() + 7)

    const menuRes = await api.get(`/api/v1/menu/?start_date=${today.toISOString()}&end_date=${end.toISOString()}`)
    menuItems.value = menuRes.data

    const recipesRes = await api.get('/api/v1/recipes/')
    recipes.value = recipesRes.data

    // Build the 7-day structure
    const days = []
    for (let i = 0; i < 7; i++) {
      const date = new Date(today)
      date.setDate(date.getDate() + i)
      const dateStr = date.toISOString().split('T')[0]
      
      const dayMeals = menuItems.value.filter(item => {
        const itemDateStr = new Date(item.date).toISOString().split('T')[0]
        return itemDateStr === dateStr
      })

      const rawDayName = date.toLocaleDateString('ru-RU', { weekday: 'long' })
      const capitalizedDayName = rawDayName.charAt(0).toUpperCase() + rawDayName.slice(1)

      days.push({
        date,
        dateStr,
        dayName: capitalizedDayName,
        dateFormatted: date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' }),
        meals: dayMeals
      })
    }
    
    weekDays.value = days
  } catch (err) {
    error.value = 'Не удалось загрузить планировщик меню'
  } finally {
    loading.value = false
  }
}

const openAddDialog = (date) => {
  showAddDialog.value = true
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
    alert(err.response?.data?.detail || 'Не удалось запланировать блюдо')
  }
}

const removeMeal = async (id) => {
  try {
    await api.delete(`/api/v1/menu/${id}`)
    await loadMenu()
  } catch (err) {
    error.value = 'Не удалось удалить блюдо из меню'
  }
}

onMounted(() => {
  loadMenu()
})
</script>
