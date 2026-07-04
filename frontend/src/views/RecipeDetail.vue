<template>
  <div class="space-y-8">
    <!-- Back Button -->
    <div>
      <router-link to="/recipes" class="text-xs font-semibold text-slate-400 hover:text-brand-400 transition flex items-center gap-1">
        &larr; Назад к каталогу рецептов
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
              {{ recipe.is_public ? 'Публичный' : 'Личный' }}
            </span>
            <div class="text-xs text-slate-500 font-semibold">
              Автор рецепта: <span class="text-slate-300">@{{ recipe.author_username || 'аноним' }}</span>
            </div>
          </div>

          <h2 class="text-3xl font-extrabold text-slate-100 tracking-tight mb-4">
            {{ recipe.title }}
          </h2>

          <div class="flex flex-wrap gap-2.5">
            <!-- Delete Button (Only for Author) -->
            <button 
              v-if="isAuthor"
              @click="deleteRecipe" 
              class="px-4 py-2 rounded-xl border border-rose-950/20 bg-rose-950/5 text-rose-400 hover:bg-rose-950/15 hover:text-rose-300 transition text-xs font-semibold"
            >
              Удалить рецепт
            </button>
            <button 
              @click="showScheduleDialog = true"
              class="px-4 py-2 rounded-xl border border-slate-800 bg-slate-900/40 text-brand-400 hover:bg-slate-850 hover:text-brand-300 transition text-xs font-semibold"
            >
              Запланировать
            </button>
            <button 
              @click="showShareDialog = true"
              class="px-4 py-2 rounded-xl border border-slate-800 bg-slate-900/40 text-brand-400 hover:bg-slate-850 hover:text-brand-300 transition text-xs font-semibold"
            >
              Поделиться
            </button>
            <button 
              @click="showRequestDialog = true"
              class="px-4 py-2 rounded-xl gradient-btn text-white text-xs font-semibold"
            >
              Попросить приготовить
            </button>
          </div>
        </div>

        <!-- Description Panel -->
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-lg font-bold text-slate-200">О рецепте</h3>
          <p class="text-slate-400 leading-relaxed text-sm">
            {{ recipe.description || 'Описание отсутствует.' }}
          </p>

          <!-- KBJU details -->
          <div v-if="recipe.total_kbju" class="border-t border-slate-800/45 pt-4 space-y-4">
            <div>
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2.5">Пищевая ценность (весь рецепт):</p>
              <div class="grid grid-cols-4 gap-3 text-center">
                <div class="p-3 rounded-xl bg-slate-900/35 border border-slate-850">
                  <p class="text-[10px] text-slate-500 font-bold uppercase">Калории</p>
                  <p class="text-base font-bold text-slate-100 mt-1">{{ Math.round(recipe.total_kbju.calories) }}</p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/35 border border-slate-850">
                  <p class="text-[10px] text-emerald-500/80 font-bold uppercase">Белки</p>
                  <p class="text-base font-bold text-emerald-400 mt-1">{{ recipe.total_kbju.proteins }}г</p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/35 border border-slate-850">
                  <p class="text-[10px] text-amber-500/80 font-bold uppercase">Жиры</p>
                  <p class="text-base font-bold text-amber-400 mt-1">{{ recipe.total_kbju.fats }}г</p>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/35 border border-slate-850">
                  <p class="text-[10px] text-indigo-500/80 font-bold uppercase">Углеводы</p>
                  <p class="text-base font-bold text-indigo-400 mt-1">{{ recipe.total_kbju.carbohydrates }}г</p>
                </div>
              </div>
            </div>

            <!-- Per 100g -->
            <div v-if="recipe.kbju_100g">
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2.5">На 100г готового блюда:</p>
              <div class="flex gap-4 text-xs font-semibold text-slate-400">
                <span>Калории: <strong class="text-slate-200">{{ Math.round(recipe.kbju_100g.calories) }} ккал</strong></span>
                <span>Б: <strong class="text-emerald-400">{{ recipe.kbju_100g.proteins }}г</strong></span>
                <span>Ж: <strong class="text-amber-400">{{ recipe.kbju_100g.fats }}г</strong></span>
                <span>У: <strong class="text-indigo-400">{{ recipe.kbju_100g.carbohydrates }}г</strong></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Instruction Panel -->
        <div class="p-6 rounded-2xl glass-panel space-y-3">
          <h3 class="text-lg font-bold text-slate-200">Инструкция по приготовлению</h3>
          <p class="text-slate-350 leading-relaxed text-sm whitespace-pre-line">
            {{ recipe.instruction || 'Инструкция по приготовлению не добавлена.' }}
          </p>
        </div>
      </div>

      <!-- Right Col: Pantry stock matching -->
      <div class="space-y-6">
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-lg font-bold text-slate-200">Наличие ингредиентов</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Мы сопоставили ингредиенты этого рецепта с вашими запасами на кухне.
          </p>

          <div v-if="recipe.smart_match" class="space-y-4">
            <!-- Global Match status -->
            <div 
              class="p-4 rounded-xl text-center text-sm font-bold border"
              :class="recipe.smart_match.can_cook 
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                : 'bg-rose-500/10 text-rose-400 border-rose-500/20'"
            >
              <span v-if="recipe.smart_match.can_cook">У вас есть все ингредиенты! Можно готовить.</span>
              <span v-else>Не хватает {{ 100 - recipe.smart_match.match_percentage }}% ингредиентов</span>
            </div>

            <!-- Ingredients checklist -->
            <div class="space-y-3">
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Список ингредиентов:</p>
              
              <div 
                v-for="item in recipe.smart_match.ingredients" 
                :key="item.product_id"
                class="p-3 rounded-xl bg-slate-900/30 border border-slate-850 flex flex-col gap-1.5"
              >
                <div class="flex justify-between items-center text-xs">
                  <span class="font-bold text-slate-200">{{ item.product_name }}</span>
                  <span class="text-slate-400 font-semibold">Нужно: {{ item.required_weight_g }}г</span>
                </div>
                
                <!-- Matching details -->
                <div class="flex justify-between items-center text-[11px] font-medium border-t border-slate-900 pt-1.5">
                  <span class="text-slate-500">В наличии: {{ item.available_weight_g }}г</span>
                  
                  <span 
                    v-if="item.is_sufficient"
                    class="text-emerald-400 font-bold uppercase tracking-wider text-[9px]"
                  >
                    В наличии
                  </span>
                  <span 
                    v-else
                    class="text-rose-400 font-bold uppercase tracking-wider text-[9px]"
                  >
                    Не хватает: {{ item.missing_weight_g }}г
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialogs / Modals -->

    <!-- Schedule Dialog -->
    <div v-if="showScheduleDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Запланировать это блюдо</h3>
        
        <form @submit.prevent="scheduleRecipe" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Выберите дату</label>
            <input 
              v-model="scheduleForm.date" 
              type="date" 
              required 
              class="w-full px-4 py-3 rounded-xl glass-input text-sm font-semibold"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Прием пищи</label>
            <select 
              v-model="scheduleForm.meal_type" 
              required
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            >
              <option value="Breakfast">Завтрак</option>
              <option value="Lunch">Обед</option>
              <option value="Dinner">Ужин</option>
              <option value="Snack">Перекус</option>
            </select>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="showScheduleDialog = false"
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

    <!-- Share Dialog -->
    <div v-if="showShareDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-2">Поделиться рецептом</h3>
        <p class="text-xs text-slate-400 mb-4">Введите имя пользователя, с которым хотите поделиться рецептом. Он сможет просматривать его и сопоставлять со своей кладовой.</p>
        
        <form @submit.prevent="shareRecipe" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Имя пользователя</label>
            <input 
              v-model="shareForm.username" 
              type="text" 
              required 
              placeholder="например: ivan_doe"
              class="w-full px-4 py-3 rounded-xl glass-input text-sm font-semibold"
            />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="showShareDialog = false"
              class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 text-sm font-semibold transition"
            >
              Отмена
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold shadow-lg shadow-brand-800/25"
            >
              Поделиться
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Cooking Request Dialog -->
    <div v-if="showRequestDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-2">Запрос на приготовление</h3>
        <p class="text-xs text-slate-400 mb-4">Попросите другого пользователя приготовить это блюдо для вас. В случае согласия оно будет добавлено в его планировщик.</p>
        
        <form @submit.prevent="sendRequest" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Имя пользователя</label>
            <input 
              v-model="requestForm.username" 
              type="text" 
              required 
              placeholder="например: masha_chef"
              class="w-full px-4 py-3 rounded-xl glass-input text-sm font-semibold"
            />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="showRequestDialog = false"
              class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 text-sm font-semibold transition"
            >
              Отмена
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold shadow-lg shadow-brand-800/25"
            >
              Отправить запрос
            </button>
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
const recipe = ref(null)
const error = ref(null)

const showScheduleDialog = ref(false)
const scheduleForm = ref({
  date: '',
  meal_type: 'Breakfast'
})

const showShareDialog = ref(false)
const shareForm = ref({
  username: ''
})

const showRequestDialog = ref(false)
const requestForm = ref({
  username: ''
})

const isAuthor = computed(() => {
  if (!recipe.value) return false
  return recipe.value.author_username === authStore.username
})

const loadRecipe = async () => {
  loading.value = true
  try {
    const response = await api.get(`/api/v1/recipes/${route.params.id}`)
    recipe.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Не удалось загрузить детали рецепта'
  } finally {
    loading.value = false
  }
}

const deleteRecipe = async () => {
  if (!confirm('Вы уверены, что хотите удалить этот рецепт?')) return
  try {
    await api.delete(`/api/v1/recipes/${route.params.id}`)
    router.push('/recipes')
  } catch (err) {
    error.value = 'Не удалось удалить рецепт'
  }
}

const scheduleRecipe = async () => {
  try {
    const datetimeStr = new Date(scheduleForm.value.date).toISOString()
    await api.post('/api/v1/menu/', {
      date: datetimeStr,
      meal_type: scheduleForm.value.meal_type,
      recipe_id: route.params.id
    })
    showScheduleDialog.value = false
    alert('Рецепт успешно запланирован!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Не удалось запланировать рецепт')
  }
}

const shareRecipe = async () => {
  try {
    await api.post('/api/v1/shares/', {
      shared_with_username: shareForm.value.username,
      recipe_id: route.params.id
    })
    showShareDialog.value = false
    alert('Рецепт успешно опубликован для пользователя!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Не удалось поделиться рецептом')
  }
}

const sendRequest = async () => {
  try {
    await api.post('/api/v1/cooking-requests/', {
      receiver_username: requestForm.value.username,
      recipe_id: route.params.id
    })
    showRequestDialog.value = false
    alert('Запрос на приготовление успешно отправлен!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Не удалось отправить запрос')
  }
}

onMounted(() => {
  loadRecipe()
})
</script>
