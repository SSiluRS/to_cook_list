<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Социальная панель
        </h1>
        <p class="text-slate-400 text-sm mt-1">Управляйте общими рецептами и запросами на приготовление еды с другими пользователями.</p>
      </div>

      <div class="flex gap-2">
        <button 
          @click="showShareDialog = true" 
          class="px-4 py-2 rounded-xl border border-slate-800 bg-slate-900/40 text-slate-300 hover:text-white transition text-xs font-semibold"
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

    <!-- Tab navigation -->
    <div class="flex items-center gap-4 border-b border-slate-800/40 pb-4">
      <button 
        @click="activeTab = 'shares'"
        class="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition border"
        :class="activeTab === 'shares' 
          ? 'bg-slate-800 border-slate-700 text-brand-400 font-bold' 
          : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'"
      >
        Доступ к рецептам
      </button>
      <button 
        @click="activeTab = 'requests'"
        class="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition border"
        :class="activeTab === 'requests' 
          ? 'bg-slate-800 border-slate-700 text-brand-400 font-bold' 
          : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'"
      >
        Запросы на готовку
      </button>
    </div>

    <!-- Alert Banner -->
    <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <!-- Loading spinner -->
    <div v-if="loading" class="py-12 flex justify-center">
      <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
    </div>

    <!-- Tab 1: Shares Content -->
    <div v-else-if="activeTab === 'shares'" class="space-y-6">
      <div class="glass-panel rounded-2xl overflow-hidden">
        <div class="p-5 border-b border-slate-800/40 bg-slate-900/10">
          <h3 class="font-bold text-slate-200 text-base">Рецепты, которыми вы поделились</h3>
        </div>

        <div v-if="myShares.length === 0" class="py-12 text-center text-slate-500 text-sm">
          <p>Вы пока ни с кем не делились рецептами.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-800/60 bg-slate-900/20 text-xs uppercase tracking-wider font-semibold text-slate-400">
                <th class="p-4 pl-6">Название рецепта</th>
                <th class="p-4">Доступ предоставлен</th>
                <th class="p-4 pr-6 text-right">Действия</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/40 text-sm text-slate-300">
              <tr 
                v-for="share in myShares" 
                :key="share.id"
                class="hover:bg-slate-900/20 transition-colors"
              >
                <td class="p-4 pl-6 font-bold text-slate-200">
                  <router-link :to="`/recipes/${share.recipe_id}`" class="hover:text-brand-400 transition">{{ share.recipe_title }}</router-link>
                </td>
                <td class="p-4 font-semibold text-brand-400">@{{ share.shared_with_username }}</td>
                <td class="p-4 pr-6 text-right">
                  <button 
                    @click="revokeShare(share.id)"
                    class="text-xs text-rose-400 hover:text-rose-300 font-bold border border-rose-950/30 hover:border-rose-900 bg-rose-950/10 px-3 py-1.5 rounded-lg transition"
                  >
                    Отозвать доступ
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Tab 2: Requests Content -->
    <div v-else-if="activeTab === 'requests'" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Incoming Requests -->
      <div class="glass-panel rounded-2xl overflow-hidden flex flex-col justify-between">
        <div>
          <div class="p-5 border-b border-slate-800/40 bg-slate-900/10">
            <h3 class="font-bold text-slate-200 text-base">Входящие запросы</h3>
          </div>

          <div v-if="incomingRequests.length === 0" class="py-12 text-center text-slate-500 text-sm">
            <p>Нет входящих запросов от других пользователей.</p>
          </div>

          <div v-else class="divide-y divide-slate-800/30">
            <div 
              v-for="req in incomingRequests" 
              :key="req.id"
              class="p-5 hover:bg-slate-900/10 transition flex items-center justify-between gap-4"
            >
              <div>
                <div class="flex items-center gap-2 mb-1.5">
                  <span class="font-bold text-slate-200 text-sm">@{{ req.sender_username }}</span>
                  <span class="text-xs text-slate-500">просит приготовить:</span>
                </div>
                <h4 class="font-extrabold text-brand-400 text-sm hover:underline">
                  <router-link :to="`/recipes/${req.recipe_id}`">{{ req.recipe_title }}</router-link>
                </h4>
                
                <!-- Status badge -->
                <span 
                  class="mt-2 inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider"
                  :class="{
                    'bg-amber-500/10 text-amber-400 border border-amber-500/20': req.status === 'Pending',
                    'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': req.status === 'Accepted',
                    'bg-rose-500/10 text-rose-400 border border-rose-500/20': req.status === 'Declined',
                  }"
                >
                  {{ translateStatus(req.status) }}
                </span>
              </div>

              <!-- Accept / Decline controls if Pending -->
              <div v-if="req.status === 'Pending'" class="flex gap-2 shrink-0">
                <button @click="respondToRequest(req.id, 'Declined')" class="px-3 py-1.5 rounded-lg border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-rose-400 text-xs font-semibold transition">
                  Отклонить
                </button>
                <button @click="respondToRequest(req.id, 'Accepted')" class="px-3 py-1.5 rounded-lg gradient-btn text-white text-xs font-semibold shadow transition">
                  Принять
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Outgoing Requests -->
      <div class="glass-panel rounded-2xl overflow-hidden">
        <div class="p-5 border-b border-slate-800/40 bg-slate-900/10">
          <h3 class="font-bold text-slate-200 text-base">Исходящие запросы</h3>
        </div>

        <div v-if="outgoingRequests.length === 0" class="py-12 text-center text-slate-500 text-sm">
          <p>Вы пока не отправляли запросов на приготовление.</p>
        </div>

        <div v-else class="divide-y divide-slate-800/30">
          <div 
            v-for="req in outgoingRequests" 
            :key="req.id"
            class="p-5 hover:bg-slate-900/10 transition flex items-center justify-between gap-4"
          >
            <div>
              <div class="flex items-center gap-2 mb-1.5">
                <span class="text-xs text-slate-500">Запрос к:</span>
                <span class="font-bold text-slate-200 text-sm">@{{ req.receiver_username }}</span>
              </div>
              <h4 class="font-extrabold text-brand-400 text-sm hover:underline">
                <router-link :to="`/recipes/${req.recipe_id}`">{{ req.recipe_title }}</router-link>
              </h4>
            </div>

            <div>
              <span 
                class="px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider border"
                :class="{
                  'bg-amber-500/10 text-amber-400 border-amber-500/20': req.status === 'Pending',
                  'bg-emerald-500/10 text-emerald-400 border-emerald-500/20': req.status === 'Accepted',
                  'bg-rose-500/10 text-rose-400 border-rose-500/20': req.status === 'Declined',
                }"
              >
                {{ translateStatus(req.status) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->

    <!-- Share Dialog -->
    <div v-if="showShareDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Поделиться доступом к рецепту</h3>
        
        <form @submit.prevent="shareRecipe" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Выберите рецепт</label>
            <select 
              v-model="shareForm.recipe_id" 
              required
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            >
              <option value="" disabled>-- Выберите рецепт --</option>
              <option 
                v-for="rec in myRecipes" 
                :key="rec.id" 
                :value="rec.id"
              >
                {{ rec.title }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Имя пользователя (кому открыть доступ)</label>
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

    <!-- Request Dialog -->
    <div v-if="showRequestDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative animate-scale-in">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Отправить запрос на приготовление</h3>
        
        <form @submit.prevent="sendRequest" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Выберите рецепт</label>
            <select 
              v-model="requestForm.recipe_id" 
              required
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            >
              <option value="" disabled>-- Выберите рецепт --</option>
              <!-- Can request any recipe the user has access to -->
              <option 
                v-for="rec in recipes" 
                :key="rec.id" 
                :value="rec.id"
              >
                {{ rec.title }} (автор: @{{ rec.author_username }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Имя кулинара (кого попросить приготовить)</label>
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
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const loading = ref(true)
const activeTab = ref('shares')
const error = ref(null)

const myShares = ref([])
const incomingRequests = ref([])
const outgoingRequests = ref([])
const myRecipes = ref([])
const recipes = ref([])

const showShareDialog = ref(false)
const shareForm = ref({
  recipe_id: '',
  username: ''
})

const showRequestDialog = ref(false)
const requestForm = ref({
  recipe_id: '',
  username: ''
})

const translateStatus = (status) => {
  const translations = {
    'Pending': 'Ожидает',
    'Accepted': 'Принят',
    'Declined': 'Отклонен'
  }
  return translations[status] || status
}

const loadSocialData = async () => {
  loading.value = true
  try {
    // Load general recipes for options list
    const recipesRes = await api.get('/api/v1/recipes/')
    recipes.value = recipesRes.data

    // Load shares
    const sharesRes = await api.get('/api/v1/shares/')
    const allShares = sharesRes.data
    // Filter shares where current user is the owner
    myShares.value = allShares.filter(s => s.owner_username === authStore.username)

    // Load cooking requests
    const reqRes = await api.get('/api/v1/cooking-requests/')
    const allReqs = reqRes.data
    incomingRequests.value = allReqs.filter(r => r.receiver_username === authStore.username)
    outgoingRequests.value = allReqs.filter(r => r.sender_username === authStore.username)

    // Load user's recipes for sharing select box
    myRecipes.value = recipes.value.filter(r => r.author_username === authStore.username)

  } catch (err) {
    error.value = 'Не удалось загрузить данные социальной панели'
  } finally {
    loading.value = false
  }
}

const shareRecipe = async () => {
  try {
    await api.post('/api/v1/shares/', {
      shared_with_username: shareForm.value.username,
      recipe_id: shareForm.value.recipe_id
    })
    showShareDialog.value = false
    await loadSocialData()
    alert('Доступ к рецепту успешно предоставлен!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Не удалось поделиться рецептом')
  }
}

const sendRequest = async () => {
  try {
    await api.post('/api/v1/cooking-requests/', {
      receiver_username: requestForm.value.username,
      recipe_id: requestForm.value.recipe_id
    })
    showRequestDialog.value = false
    await loadSocialData()
    alert('Запрос на приготовление успешно отправлен!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Не удалось отправить запрос')
  }
}

const respondToRequest = async (id, status) => {
  try {
    await api.patch(`/api/v1/cooking-requests/${id}`, { status })
    await loadSocialData()
  } catch (err) {
    error.value = 'Не удалось ответить на запрос'
  }
}

const revokeShare = async (id) => {
  try {
    await api.delete(`/api/v1/shares/${id}`)
    await loadSocialData()
  } catch (err) {
    error.value = 'Не удалось отозвать доступ к рецепту'
  }
}

onMounted(() => {
  loadSocialData()
})
</script>
