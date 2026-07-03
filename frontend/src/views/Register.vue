<template>
  <div class="h-full flex items-center justify-center">
    <div class="w-full max-w-md p-8 rounded-2xl glass-card border border-slate-800/60 shadow-2xl relative overflow-hidden">
      <!-- Glow effect -->
      <div class="absolute -top-16 -left-16 w-32 h-32 bg-brand-500/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-16 -right-16 w-32 h-32 bg-brand-600/15 rounded-full blur-3xl"></div>

      <div class="text-center mb-8 relative">
        <h2 class="text-2xl font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">Создать аккаунт</h2>
        <p class="text-sm text-slate-400 mt-1">Планируйте свое питание с умным подбором рецептов</p>
      </div>

      <!-- Error Alert -->
      <div v-if="authStore.error" class="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center gap-3">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 shrink-0">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
        </svg>
        <span>{{ translateError(authStore.error) }}</span>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Имя пользователя</label>
          <input 
            v-model="username" 
            type="text" 
            required 
            placeholder="ivan_ivanov"
            class="w-full px-4 py-3 rounded-xl glass-input text-sm"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Email адрес</label>
          <input 
            v-model="email" 
            type="email" 
            required 
            placeholder="ivan@example.com"
            class="w-full px-4 py-3 rounded-xl glass-input text-sm"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Пароль</label>
          <input 
            v-model="password" 
            type="password" 
            required 
            placeholder="••••••••"
            class="w-full px-4 py-3 rounded-xl glass-input text-sm"
          />
        </div>

        <button 
          type="submit" 
          :disabled="authStore.loading"
          class="w-full py-3 rounded-xl gradient-btn text-sm font-semibold text-white shadow-lg shadow-brand-700/25 flex items-center justify-center gap-2"
        >
          <span v-if="authStore.loading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span>{{ authStore.loading ? 'Создание аккаунта...' : 'Зарегистрироваться' }}</span>
        </button>
      </form>

      <div class="mt-8 text-center text-sm text-slate-400">
        Уже есть аккаунт? 
        <router-link to="/login" class="text-brand-400 hover:text-brand-300 font-semibold transition ml-1">Войти</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')

const translateError = (err) => {
  if (!err) return ''
  if (err.includes('Username already registered')) return 'Это имя пользователя уже занято'
  return err
}

const handleRegister = async () => {
  const success = await authStore.register(username.value, email.value, password.value)
  if (success) {
    router.push('/dashboard')
  }
}
</script>
