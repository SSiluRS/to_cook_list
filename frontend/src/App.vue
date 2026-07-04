<template>
  <div class="min-h-screen bg-[#07090b] text-[#f1f5f9] flex">
    <!-- Mobile Overlay Backdrop -->
    <div
      v-if="authStore.isAuthenticated && mobileMenuOpen"
      class="fixed inset-0 bg-black/60 z-40 lg:hidden"
      @click="mobileMenuOpen = false"
    ></div>

    <!-- Sidebar for Authenticated Users -->
    <aside
      v-if="authStore.isAuthenticated"
      class="fixed lg:static inset-y-0 left-0 w-64 glass-panel border-r border-slate-800/40 flex flex-col justify-between shrink-0 z-50 transition-transform duration-300 lg:translate-x-0"
      :class="mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-6">
        <!-- App Title / Logo -->
        <div class="flex items-center gap-3 mb-8">
          <div class="w-10 h-10 rounded-xl gradient-btn flex items-center justify-center shadow-lg shadow-brand-800/20">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6 text-white">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.044l4.5-2.251m0 0l4.5-2.251m-9 4.502L7.5 15.793m0 0L3 13.541M12 18.044V21m0-2.956L7.5 15.793m0 0v-3.07M12 18.044l4.5-2.251m0-3.071L12 15m0 0L7.5 12.722m4.5 2.278V12m0 0L16.5 9.75M12 12L7.5 9.75M16.5 9.75v-3.07L12 4.43m4.5 2.25L21 4.43m-9 0L7.5 6.68m0 0L3 4.43m4.5 2.25v3.07" />
            </svg>
          </div>
          <div>
            <h2 class="font-bold text-lg tracking-wide bg-gradient-to-r from-slate-100 to-slate-400 bg-clip-text text-transparent">To Cook List</h2>
            <p class="text-xs text-slate-500 font-medium">Кулинарный навигатор</p>
          </div>
          <!-- Close button for mobile sidebar -->
          <button @click="mobileMenuOpen = false" class="ml-auto lg:hidden p-1 text-slate-400 hover:text-white transition">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Navigation Links -->
        <nav class="space-y-1">
          <router-link @click="mobileMenuOpen = false" to="/dashboard" class="flex items-center gap-3 px-4 py-3 rounded-xl transition text-slate-400 hover:text-slate-100 hover:bg-slate-800/30" active-class="bg-slate-800/40 text-brand-400 border border-slate-700/20 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
            Панель управления
          </router-link>
          
          <router-link @click="mobileMenuOpen = false" to="/pantry" class="flex items-center gap-3 px-4 py-3 rounded-xl transition text-slate-400 hover:text-slate-100 hover:bg-slate-800/30" active-class="bg-slate-800/40 text-brand-400 border border-slate-700/20 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
            </svg>
            Моя кладовая
          </router-link>

          <router-link @click="mobileMenuOpen = false" to="/products" class="flex items-center gap-3 px-4 py-3 rounded-xl transition text-slate-400 hover:text-slate-100 hover:bg-slate-800/30" active-class="bg-slate-800/40 text-brand-400 border border-slate-700/20 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75M3.75 10.125v3.75m16.5 0v3.75m-16.5-3.75v3.75" />
            </svg>
            Справочник КБЖУ
          </router-link>

          <router-link @click="mobileMenuOpen = false" to="/recipes" class="flex items-center gap-3 px-4 py-3 rounded-xl transition text-slate-400 hover:text-slate-100 hover:bg-slate-800/30" active-class="bg-slate-800/40 text-brand-400 border border-slate-700/20 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
            </svg>
            Рецепты
          </router-link>

          <router-link @click="mobileMenuOpen = false" to="/menu" class="flex items-center gap-3 px-4 py-3 rounded-xl transition text-slate-400 hover:text-slate-100 hover:bg-slate-800/30" active-class="bg-slate-800/40 text-brand-400 border border-slate-700/20 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
            </svg>
            Планировщик
          </router-link>

          <router-link @click="mobileMenuOpen = false" to="/social" class="flex items-center gap-3 px-4 py-3 rounded-xl transition text-slate-400 hover:text-slate-100 hover:bg-slate-800/30" active-class="bg-slate-800/40 text-brand-400 border border-slate-700/20 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.097-4.012l-.02-.022a11.942 11.942 0 017.227-2.316c2.617 0 5.078.836 7.094 2.262m-10.94-7.82c0 2.485-2.099 4.5-4.688 4.5-2.588 0-4.687-2.015-4.687-4.5S4.812 3 7.5 3s4.688 2.015 4.688 4.5zm8.438 0c0 2.485-2.099 4.5-4.688 4.5-2.588 0-4.687-2.015-4.687-4.5S13.812 3 16.5 3s4.688 2.015 4.688 4.5z" />
            </svg>
            Социальная панель
          </router-link>
        </nav>
      </div>

      <!-- User Profile & Logout -->
      <div class="p-6 border-t border-slate-800/40 bg-slate-900/10">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center font-bold text-brand-400 border border-slate-700/50">
            {{ authStore.username ? authStore.username[0].toUpperCase() : 'U' }}
          </div>
          <div class="truncate">
            <p class="text-sm font-semibold text-slate-200">{{ authStore.username || 'Пользователь' }}</p>
            <p class="text-xs text-slate-500 truncate">В сети</p>
          </div>
        </div>
        <button @click="logout" class="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border border-slate-800 text-slate-400 hover:text-rose-400 hover:border-rose-950/30 hover:bg-rose-950/10 transition text-sm font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
          </svg>
          Выйти
        </button>
      </div>
    </aside>

    <!-- Main View Area -->
    <main class="flex-1 flex flex-col min-w-0">
      <!-- Navbar / Top Header for Authenticated Users -->
      <header v-if="authStore.isAuthenticated" class="h-14 lg:h-16 border-b border-slate-800/30 px-4 lg:px-8 flex items-center justify-between glass-panel sticky top-0 z-30">
        <!-- Mobile hamburger button -->
        <button @click="mobileMenuOpen = true" class="lg:hidden p-2 -ml-2 text-slate-400 hover:text-white transition">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
        <h1 class="text-base lg:text-lg font-bold bg-gradient-to-r from-slate-200 to-slate-400 bg-clip-text text-transparent truncate">
          {{ currentRouteName }}
        </h1>
        <div class="text-xs lg:text-sm text-slate-400 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="hidden sm:inline">Подключено к API</span>
        </div>
      </header>

      <!-- Router Content -->
      <div class="flex-1 p-4 lg:p-8 overflow-y-auto pb-20 lg:pb-8">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- Mobile Bottom Navigation Bar -->
    <nav v-if="authStore.isAuthenticated" class="fixed bottom-0 left-0 right-0 z-30 lg:hidden glass-panel border-t border-slate-800/40">
      <div class="flex items-center justify-around h-16 px-1">
        <router-link
          v-for="item in bottomNavItems"
          :key="item.to"
          :to="item.to"
          class="flex flex-col items-center justify-center gap-0.5 px-2 py-1 rounded-lg transition text-slate-500 min-w-0"
          active-class="text-brand-400"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="text-[10px] font-semibold truncate">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, h, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

// Close mobile menu on route change
watch(() => route.path, () => {
  mobileMenuOpen.value = false
})

const routeNameTranslations = {
  'Dashboard': 'Панель управления',
  'Pantry': 'Моя кладовая',
  'Products': 'Справочник КБЖУ',
  'Recipes': 'Рецепты',
  'RecipeDetail': 'Рецепт детально',
  'Menu': 'Планировщик меню',
  'Social': 'Социальная панель',
  'Login': 'Вход',
  'Register': 'Регистрация'
}

const currentRouteName = computed(() => {
  const name = route.name || 'Dashboard'
  return routeNameTranslations[name] || name
})

// SVG icon components for bottom nav
const HomeIcon = (_, { attrs }) => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', 'stroke-width': '2', stroke: 'currentColor', ...attrs }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25' })
])
const PantryIcon = (_, { attrs }) => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', 'stroke-width': '2', stroke: 'currentColor', ...attrs }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z' })
])
const RecipeIcon = (_, { attrs }) => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', 'stroke-width': '2', stroke: 'currentColor', ...attrs }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25' })
])
const MenuIcon = (_, { attrs }) => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', 'stroke-width': '2', stroke: 'currentColor', ...attrs }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5' })
])
const SocialIcon = (_, { attrs }) => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', 'stroke-width': '2', stroke: 'currentColor', ...attrs }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z' })
])

const bottomNavItems = [
  { to: '/dashboard', label: 'Главная', icon: HomeIcon },
  { to: '/pantry', label: 'Кладовая', icon: PantryIcon },
  { to: '/recipes', label: 'Рецепты', icon: RecipeIcon },
  { to: '/menu', label: 'Меню', icon: MenuIcon },
  { to: '/social', label: 'Соц.панель', icon: SocialIcon },
]

const logout = () => {
  mobileMenuOpen.value = false
  authStore.logout()
  router.push('/login')
}
</script>

<style>
/* Smooth fade transition for views */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
