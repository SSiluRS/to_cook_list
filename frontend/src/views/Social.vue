<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Social Board
        </h1>
        <p class="text-slate-400 text-sm mt-1">Manage recipe shares and "Cook for me" requests with other users.</p>
      </div>

      <div class="flex gap-2">
        <button 
          @click="showShareDialog = true" 
          class="px-4 py-2 rounded-xl border border-slate-800 bg-slate-900/40 text-slate-300 hover:text-white transition text-xs font-semibold"
        >
          Share Recipe
        </button>
        <button 
          @click="showRequestDialog = true" 
          class="px-4 py-2 rounded-xl gradient-btn text-white text-xs font-semibold"
        >
          Request Cooking
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
        Shared Recipes
      </button>
      <button 
        @click="activeTab = 'requests'"
        class="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition border"
        :class="activeTab === 'requests' 
          ? 'bg-slate-800 border-slate-700 text-brand-400 font-bold' 
          : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'"
      >
        Cooking Requests
      </button>
    </div>

    <!-- Alert Banner -->
    <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
      {{ error }}
    </div>

    <div v-if="loading" class="py-12 flex justify-center">
      <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
    </div>

    <div v-else class="space-y-6">
      <!-- 1. Shared Access Tab -->
      <div v-if="activeTab === 'shares'" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Shared by me -->
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2">Recipes I Shared</h3>
          <div v-if="sharedByMe.length === 0" class="py-8 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl text-xs">
            You haven't shared any recipes yet.
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="s in sharedByMe" 
              :key="s.id"
              class="p-4 rounded-xl glass-card flex items-center justify-between gap-4 text-sm"
            >
              <div>
                <h4 class="font-bold text-slate-200">
                  <router-link :to="`/recipes/${s.recipe_id}`" class="hover:text-brand-400 transition">{{ s.recipe_title }}</router-link>
                </h4>
                <p class="text-xs text-slate-500 mt-1">Shared with @{{ s.shared_with_username }}</p>
              </div>
              <button 
                @click="revokeShare(s.id)"
                class="px-2.5 py-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-rose-400 hover:bg-rose-950/20 hover:border-rose-950/20 transition text-xs font-semibold"
              >
                Revoke
              </button>
            </div>
          </div>
        </div>

        <!-- Shared with me -->
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2">Recipes Shared With Me</h3>
          <div v-if="sharedWithMe.length === 0" class="py-8 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl text-xs">
            No recipes shared with you.
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="s in sharedWithMe" 
              :key="s.id"
              class="p-4 rounded-xl glass-card flex items-center justify-between gap-4 text-sm"
            >
              <div>
                <h4 class="font-bold text-slate-200">
                  <router-link :to="`/recipes/${s.recipe_id}`" class="hover:text-brand-400 transition">{{ s.recipe_title }}</router-link>
                </h4>
                <p class="text-xs text-slate-500 mt-1">Owned by @{{ s.owner_username }}</p>
              </div>
              <button 
                @click="revokeShare(s.id)"
                class="px-2.5 py-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-slate-200 transition text-xs font-semibold"
              >
                Hide
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Cooking Requests Tab -->
      <div v-if="activeTab === 'requests'" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Inbox: Incoming cooking requests -->
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2">Inbox (Requested from me)</h3>
          <div v-if="incomingRequests.length === 0" class="py-8 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl text-xs">
            No incoming cooking requests.
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="r in incomingRequests" 
              :key="r.id"
              class="p-4 rounded-xl glass-card flex flex-col gap-3 text-sm"
            >
              <div class="flex justify-between items-start">
                <div>
                  <span class="font-bold text-slate-200">@{{ r.sender_username }}</span> 
                  <span class="text-slate-500 text-xs ml-1">wants you to cook:</span>
                  <h4 class="font-bold text-slate-100 text-base mt-1">
                    <router-link :to="`/recipes/${r.recipe_id}`" class="hover:text-brand-400 transition">{{ r.recipe_title }}</router-link>
                  </h4>
                </div>
                <!-- Status badge -->
                <span 
                  class="px-2 py-1 rounded text-[10px] uppercase font-bold tracking-wider"
                  :class="{
                    'bg-slate-900 text-slate-400 border border-slate-800': r.status === 'Pending',
                    'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': r.status === 'Accepted',
                    'bg-rose-500/10 text-rose-400 border border-rose-500/20': r.status === 'Declined',
                  }"
                >
                  {{ r.status }}
                </span>
              </div>

              <!-- Action buttons for Pending requests -->
              <div v-if="r.status === 'Pending'" class="flex justify-end gap-2 border-t border-slate-850 pt-3">
                <button @click="respondToRequest(r.id, 'Declined')" class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 font-semibold text-xs transition">
                  Decline
                </button>
                <button @click="respondToRequest(r.id, 'Accepted')" class="px-3 py-1.5 rounded-lg gradient-btn text-white font-semibold text-xs transition">
                  Accept & Cook
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Outbox: Sent cooking requests -->
        <div class="p-6 rounded-2xl glass-panel space-y-4">
          <h3 class="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2">Sent Requests</h3>
          <div v-if="sentRequests.length === 0" class="py-8 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl text-xs">
            You haven't sent any cooking requests yet.
          </div>
          <div v-else class="space-y-3">
            <div 
              v-for="r in sentRequests" 
              :key="r.id"
              class="p-4 rounded-xl glass-card flex items-center justify-between gap-4 text-sm"
            >
              <div>
                <p class="text-xs text-slate-500">Sent to @{{ r.receiver_username }}</p>
                <h4 class="font-bold text-slate-200 mt-1">
                  <router-link :to="`/recipes/${r.recipe_id}`" class="hover:text-brand-400 transition">{{ r.recipe_title }}</router-link>
                </h4>
              </div>

              <span 
                class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider border"
                :class="{
                  'bg-slate-950 text-slate-500 border-slate-850': r.status === 'Pending',
                  'bg-emerald-500/10 text-emerald-400 border-emerald-500/20': r.status === 'Accepted',
                  'bg-rose-500/10 text-rose-400 border-rose-500/20': r.status === 'Declined',
                }"
              >
                {{ r.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Share Dialog -->
    <div v-if="showShareDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-sm p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Share Recipe Access</h3>
        
        <form @submit.prevent="shareRecipe" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Select Recipe</label>
            <select v-model="shareForm.recipe_id" required class="w-full px-4 py-3 rounded-xl glass-input text-sm">
              <option value="" disabled>-- Select Recipe --</option>
              <option v-for="rec in myRecipes" :key="rec.id" :value="rec.id">{{ rec.title }}</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Recipient Username or Email</label>
            <input v-model="shareForm.username" type="text" required placeholder="e.g. chef_john" class="w-full px-4 py-3 rounded-xl glass-input text-sm" />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="showShareDialog = false" class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 text-sm font-semibold transition">Cancel</button>
            <button type="submit" class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold">Share</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Request Dialog -->
    <div v-if="showRequestDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="w-full max-w-sm p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-100 mb-4">Request Cooking</h3>
        
        <form @submit.prevent="sendRequest" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Select Recipe</label>
            <select v-model="requestForm.recipe_id" required class="w-full px-4 py-3 rounded-xl glass-input text-sm">
              <option value="" disabled>-- Select Recipe --</option>
              <option v-for="rec in myRecipes" :key="rec.id" :value="rec.id">{{ rec.title }}</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Chef Username or Email</label>
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
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const loading = ref(true)
const activeTab = ref('shares')
const error = ref(null)

const sharedByMe = ref([])
const sharedWithMe = ref([])
const incomingRequests = ref([])
const sentRequests = ref([])
const myRecipes = ref([])

const showShareDialog = ref(false)
const shareForm = ref({ recipe_id: '', username: '' })

const showRequestDialog = ref(false)
const requestForm = ref({ recipe_id: '', username: '' })

const loadSocialData = async () => {
  loading.value = true
  try {
    // Load Shares
    const sharesRes = await api.get('/api/v1/shares/')
    const allShares = sharesRes.data
    sharedByMe.value = allShares.filter(s => s.owner_username === authStore.username)
    sharedWithMe.value = allShares.filter(s => s.shared_with_username === authStore.username)

    // Load Cooking Requests
    const reqRes = await api.get('/api/v1/cooking-requests/')
    const allReqs = reqRes.data
    incomingRequests.value = allReqs.filter(r => r.receiver_username === authStore.username)
    sentRequests.value = allReqs.filter(r => r.sender_username === authStore.username)

    // Load user's recipes for sharing select box
    const recipesRes = await api.get('/api/v1/recipes/')
    myRecipes.value = recipesRes.data.filter(r => r.author_username === authStore.username)

  } catch (err) {
    error.value = 'Failed to load social board data'
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
    alert('Recipe shared successfully!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to share recipe')
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
    alert('Cooking request sent successfully!')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to send cooking request')
  }
}

const respondToRequest = async (id, status) => {
  try {
    await api.patch(`/api/v1/cooking-requests/${id}`, { status })
    await loadSocialData()
  } catch (err) {
    error.value = 'Failed to respond to request'
  }
}

const revokeShare = async (id) => {
  try {
    await api.delete(`/api/v1/shares/${id}`)
    await loadSocialData()
  } catch (err) {
    error.value = 'Failed to revoke shared access'
  }
}

onMounted(() => {
  loadSocialData()
})
</script>
