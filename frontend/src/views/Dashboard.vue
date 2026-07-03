<template>
  <div class="space-y-8">
    <!-- Welcome Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Привет, {{ authStore.username }}!
        </h1>
        <p class="text-slate-400 text-sm mt-1">Вот твой кулинарный обзор на сегодня.</p>
      </div>
      <div class="flex gap-3">
        <router-link to="/recipes" class="px-5 py-2.5 rounded-xl border border-slate-800 bg-slate-900/40 text-slate-300 hover:text-white hover:bg-slate-800/40 transition text-sm font-semibold flex items-center gap-2">
          Обзор рецептов
        </router-link>
        <router-link to="/menu" class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold flex items-center gap-2">
          Планировать меню
        </router-link>
      </div>
    </div>

    <!-- Quick Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- Pantry Stock -->
      <div class="p-6 rounded-2xl glass-card relative overflow-hidden">
        <div class="absolute top-4 right-4 text-brand-400/20">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
          </svg>
        </div>
        <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Моя кладовая</p>
        <h3 class="text-3xl font-bold mt-2 text-slate-100">{{ pantryCount }}</h3>
        <p class="text-xs text-slate-400 mt-1">Ингредиентов в наличии</p>
      </div>

      <!-- Recipes -->
      <div class="p-6 rounded-2xl glass-card relative overflow-hidden">
        <div class="absolute top-4 right-4 text-brand-400/20">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
          </svg>
        </div>
        <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Всего рецептов</p>
        <h3 class="text-3xl font-bold mt-2 text-slate-100">{{ recipeCount }}</h3>
        <p class="text-xs text-slate-400 mt-1">Доступно кулинарных карт</p>
      </div>

      <!-- Today's Planned Meals -->
      <div class="p-6 rounded-2xl glass-card relative overflow-hidden">
        <div class="absolute top-4 right-4 text-brand-400/20">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
          </svg>
        </div>
        <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Блюда на сегодня</p>
        <h3 class="text-3xl font-bold mt-2 text-slate-100">{{ todayMeals.length }}</h3>
        <p class="text-xs text-slate-400 mt-1">Запланировано на сегодня</p>
      </div>

      <!-- Pending Social Actions -->
      <div class="p-6 rounded-2xl glass-card relative overflow-hidden">
        <div class="absolute top-4 right-4 text-brand-400/20">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
            <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477" />
          </svg>
        </div>
        <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Социальная активность</p>
        <h3 class="text-3xl font-bold mt-2 text-slate-100">{{ pendingRequestsCount }}</h3>
        <p class="text-xs text-slate-400 mt-1">Ожидает запросов на готовку</p>
      </div>
    </div>

    <!-- Main Grid Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column: Today's Menu -->
      <div class="lg:col-span-2 space-y-6">
        <div class="p-6 rounded-2xl glass-panel">
          <h2 class="text-lg font-bold text-slate-200 mb-4 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-brand-400">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
            </svg>
            Расписание на сегодня
          </h2>

          <div v-if="loading" class="py-8 flex justify-center">
            <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
          </div>

          <div v-else-if="todayMeals.length === 0" class="py-12 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 mx-auto text-slate-600 mb-3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-sm font-medium">На сегодня нет запланированных блюд.</p>
            <router-link to="/menu" class="text-xs text-brand-400 hover:text-brand-300 font-semibold mt-1 inline-block">Запланировать блюдо &rarr;</router-link>
          </div>

          <div v-else class="space-y-4">
            <div 
              v-for="meal in todayMeals" 
              :key="meal.id"
              class="p-4 rounded-xl glass-card flex items-center justify-between gap-4"
            >
              <div class="flex items-center gap-4">
                <!-- Meal Type Badge -->
                <span 
                  class="px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider text-center shrink-0 w-24"
                  :class="{
                    'bg-amber-500/10 text-amber-400 border border-amber-500/20': meal.meal_type === 'Breakfast',
                    'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': meal.meal_type === 'Lunch',
                    'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20': meal.meal_type === 'Dinner',
                    'bg-pink-500/10 text-pink-400 border border-pink-500/20': meal.meal_type === 'Snack',
                  }"
                >
                  {{ translateMealType(meal.meal_type) }}
                </span>
                <div>
                  <h4 class="font-bold text-slate-200 text-sm hover:text-brand-400 transition">
                    <router-link :to="`/recipes/${meal.recipe_id}`">{{ meal.recipe_title }}</router-link>
                  </h4>
                  <div v-if="meal.recipe && meal.recipe.total_kbju" class="text-xs text-slate-500 mt-1 flex gap-3 font-medium">
                    <span>Кал: {{ Math.round(meal.recipe.total_kbju.calories) }} ккал</span>
                    <span>Б: {{ meal.recipe.total_kbju.proteins }}г</span>
                    <span>Ж: {{ meal.recipe.total_kbju.fats }}г</span>
                    <span>У: {{ meal.recipe.total_kbju.carbohydrates }}г</span>
                  </div>
                </div>
              </div>
              
              <!-- Cooking match badge -->
              <div v-if="meal.recipe && meal.recipe.smart_match" class="text-right shrink-0">
                <span 
                  class="px-2.5 py-1 rounded-full text-xs font-semibold"
                  :class="meal.recipe.smart_match.can_cook ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'"
                >
                  {{ meal.recipe.smart_match.can_cook ? 'Готово' : `Не хватает ${100 - meal.recipe.smart_match.match_percentage}%` }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Pending Requests List -->
      <div class="space-y-6">
        <div class="p-6 rounded-2xl glass-panel">
          <h2 class="text-lg font-bold text-slate-200 mb-4 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-brand-400">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
            </svg>
            Входящие запросы
          </h2>

          <div v-if="loading" class="py-4 flex justify-center">
            <span class="w-6 h-6 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
          </div>

          <div v-else-if="incomingRequests.length === 0" class="py-8 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl text-xs">
            <p class="text-xs">Нет входящих запросов от других пользователей.</p>
          </div>

          <div v-else class="space-y-3">
            <div 
              v-for="req in incomingRequests" 
              :key="req.id"
              class="p-3 rounded-xl bg-slate-900/30 border border-slate-800/40 text-xs flex flex-col gap-2"
            >
              <div class="flex justify-between">
                <span class="font-bold text-slate-300">@{{ req.sender_username }}</span>
                <span class="text-slate-500 font-medium">хочет, чтобы вы приготовили:</span>
              </div>
              <div class="font-semibold text-brand-400 text-sm">
                {{ req.recipe_title || 'Общее меню' }}
              </div>
              <div class="flex justify-end gap-2 mt-1">
                <button @click="respondToRequest(req.id, 'Declined')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium transition">
                  Отклонить
                </button>
                <button @click="respondToRequest(req.id, 'Accepted')" class="px-2.5 py-1 rounded gradient-btn text-white font-medium transition">
                  Принять
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const loading = ref(true)
const pantryCount = ref(0)
const recipeCount = ref(0)
const todayMeals = ref([])
const pendingRequestsCount = ref(0)
const incomingRequests = ref([])

const translateMealType = (type) => {
  const translations = {
    'Breakfast': 'Завтрак',
    'Lunch': 'Обед',
    'Dinner': 'Ужин',
    'Snack': 'Перекус'
  }
  return translations[type] || type
}

const loadData = async () => {
  loading.value = true
  try {
    // 1. Load Pantry count
    const pantryRes = await api.get('/api/v1/pantry/')
    pantryCount.value = pantryRes.data.length

    // 2. Load Recipes count
    const recipesRes = await api.get('/api/v1/recipes/')
    recipeCount.value = recipesRes.data.length

    // 3. Load today's menu
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    
    const menuRes = await api.get(`/api/v1/menu/?start_date=${today.toISOString()}&end_date=${tomorrow.toISOString()}`)
    todayMeals.value = menuRes.data

    // 4. Load Cooking requests
    const reqRes = await api.get('/api/v1/cooking-requests/')
    const allReqs = reqRes.data
    
    // Incoming pending requests
    incomingRequests.value = allReqs.filter(r => r.receiver_username === authStore.username && r.status === 'Pending')
    pendingRequestsCount.value = incomingRequests.value.length

  } catch (err) {
    console.error('Failed to load dashboard data:', err)
  } finally {
    loading.value = false
  }
}

const respondToRequest = async (id, status) => {
  try {
    await api.patch(`/api/v1/cooking-requests/${id}`, { status })
    await loadData()
  } catch (err) {
    console.error('Failed to update request status:', err)
  }
}

onMounted(() => {
  loadData()
})
</script>
