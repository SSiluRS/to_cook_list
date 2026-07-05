<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-xl sm:text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent">
          Справочник КБЖУ
        </h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-1">Просматривайте пищевую ценность продуктов (на 100г) или добавляйте свои ингредиенты.</p>
      </div>

      <button 
        @click="showAddDialog = true" 
        class="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl gradient-btn text-white text-xs sm:text-sm font-semibold flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7-7H5" />
        </svg>
        Новый продукт
      </button>
    </div>

    <!-- Tab navigation -->
    <div class="flex items-center gap-4 border-b border-slate-800/40 pb-4">
      <button 
        @click="switchTab('local')"
        class="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition border"
        :class="activeTab === 'local' 
          ? 'bg-slate-800 border-slate-700 text-brand-400 font-bold' 
          : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'"
      >
        Локальный каталог
      </button>
      <button 
        @click="switchTab('external')"
        class="px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition border"
        :class="activeTab === 'external' 
          ? 'bg-slate-800 border-slate-700 text-brand-400 font-bold' 
          : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'"
      >
        Поиск в Интернете
      </button>
    </div>

    <!-- Local Catalog Tab -->
    <div v-if="activeTab === 'local'" class="space-y-6">
      <!-- Filter and Search Row -->
      <div class="flex items-center gap-4 max-w-md">
        <div class="relative flex-1">
          <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Поиск в локальном каталоге..."
            class="w-full pl-10 pr-4 py-2.5 rounded-xl glass-input text-xs font-semibold"
          />
        </div>
      </div>

      <!-- Alert Banner -->
      <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
        {{ error }}
      </div>

      <!-- Products List -->
      <div class="glass-panel rounded-2xl overflow-hidden">
        <div v-if="loading" class="py-12 flex justify-center">
          <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
        </div>

        <div v-else-if="filteredProducts.length === 0" class="py-16 text-center text-slate-500">
          <p class="text-base font-semibold text-slate-400">Продукты не найдены</p>
          <p class="text-sm text-slate-500 mt-1">Попробуйте изменить поисковый запрос или добавьте новый продукт.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-800/60 bg-slate-900/20 text-xs uppercase tracking-wider font-semibold text-slate-400">
                <th class="p-3 sm:p-4 pl-4 sm:pl-6">Название продукта</th>
                <th class="p-3 sm:p-4 hidden sm:table-cell">Калорийность (100г)</th>
                <th class="p-3 sm:p-4 hidden md:table-cell">Белки (100г)</th>
                <th class="p-3 sm:p-4 hidden md:table-cell">Жиры (100г)</th>
                <th class="p-3 sm:p-4 hidden md:table-cell">Углеводы (100г)</th>
                <th class="p-3 sm:p-4 pr-4 sm:pr-6 text-right">Действие</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/40 text-sm text-slate-300">
              <tr 
                v-for="prod in filteredProducts" 
                :key="prod.id"
                class="hover:bg-slate-900/20 transition-colors"
              >
                <td class="p-3 sm:p-4 pl-4 sm:pl-6 font-bold text-slate-200">
                  <div>{{ prod.name }}</div>
                  <div class="sm:hidden text-xs font-normal text-slate-400 mt-0.5">
                    {{ Math.round(prod.calories) }} ккал | Б:{{ prod.proteins }} / Ж:{{ prod.fats }} / У:{{ prod.carbohydrates }}
                  </div>
                </td>
                <td class="p-3 sm:p-4 hidden sm:table-cell font-medium">{{ Math.round(prod.calories) }} ккал</td>
                <td class="p-3 sm:p-4 hidden md:table-cell text-emerald-400 font-semibold">{{ prod.proteins }}г</td>
                <td class="p-3 sm:p-4 hidden md:table-cell text-amber-400 font-semibold">{{ prod.fats }}г</td>
                <td class="p-3 sm:p-4 hidden md:table-cell text-indigo-400 font-semibold">{{ prod.carbohydrates }}г</td>
                <td class="p-3 sm:p-4 pr-4 sm:pr-6 text-right space-x-1 sm:space-x-2">
                  <button 
                    @click="editProduct(prod)"
                    class="px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg border border-slate-800 hover:border-brand-500 hover:bg-brand-500/10 text-brand-400 hover:text-brand-300 text-xxs sm:text-xs font-semibold transition"
                  >
                    Редактировать
                  </button>
                  <button 
                    @click="deleteProduct(prod.id)"
                    class="px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg border border-slate-800 hover:border-rose-950 text-slate-400 hover:text-rose-400 hover:bg-rose-950/15 text-xxs sm:text-xs transition"
                  >
                    Удалить
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- External Internet Search Tab -->
    <div v-else-if="activeTab === 'external'" class="space-y-6">
      <div class="p-5 rounded-2xl bg-slate-900/20 border border-slate-850">
        <h3 class="font-bold text-slate-200 text-sm mb-2">Поиск по открытой базе Open Food Facts</h3>
        <p class="text-xs text-slate-400 mb-4 leading-relaxed">
          Вы можете найти любой продукт в интернете, отредактировать его параметры КБЖУ под свои нужды и импортировать в ваш личный каталог.
        </p>

        <!-- Search Bar with Go button -->
        <form @submit.prevent="searchExternal" class="flex gap-3 max-w-lg">
          <div class="relative flex-1">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </span>
            <input 
              v-model="externalQuery" 
              type="text" 
              placeholder="Введите название продукта (например: творог 5%)..."
              autocorrect="on"
              autocapitalize="sentences"
              spellcheck="true"
              class="w-full pl-10 pr-4 py-2.5 rounded-xl glass-input text-xs font-semibold"
              required
            />
          </div>
          <button 
            type="submit"
            :disabled="loadingExternal"
            class="px-5 py-2.5 rounded-xl gradient-btn text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition shrink-0"
          >
            <span v-if="loadingExternal" class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            <span>Найти</span>
          </button>
        </form>
      </div>

      <!-- Alert Banner -->
      <div v-if="error" class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm">
        {{ error }}
      </div>

      <!-- External Search Results -->
      <div class="glass-panel rounded-2xl overflow-hidden">
        <div v-if="loadingExternal" class="py-12 flex justify-center">
          <span class="w-8 h-8 border-2 border-brand-500/30 border-t-brand-500 rounded-full animate-spin"></span>
        </div>

        <div v-else-if="externalProducts.length === 0" class="py-16 text-center text-slate-500">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 mx-auto text-slate-600 mb-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-base font-semibold text-slate-400">Результаты поиска отсутствуют</p>
          <p class="text-sm text-slate-500 mt-1">Введите поисковый запрос выше, чтобы найти продукты из интернета.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-800/60 bg-slate-900/20 text-xs uppercase tracking-wider font-semibold text-slate-400">
                <th class="p-3 sm:p-4 pl-4 sm:pl-6">Продукт (из Интернета)</th>
                <th class="p-3 sm:p-4 hidden sm:table-cell">Калорийность (100г)</th>
                <th class="p-3 sm:p-4 hidden md:table-cell">Белки (100г)</th>
                <th class="p-3 sm:p-4 hidden md:table-cell">Жиры (100г)</th>
                <th class="p-3 sm:p-4 hidden md:table-cell">Углеводы (100г)</th>
                <th class="p-3 sm:p-4 pr-4 sm:pr-6 text-right">Действие</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/40 text-sm text-slate-300">
              <tr 
                v-for="(prod, idx) in externalProducts" 
                :key="idx"
                class="hover:bg-slate-900/20 transition-colors"
              >
                <td class="p-3 sm:p-4 pl-4 sm:pl-6 font-bold text-slate-200">
                  <div class="line-clamp-1 max-w-[180px] sm:max-w-[280px]" :title="prod.name">{{ prod.name }}</div>
                  <div class="sm:hidden text-xs font-normal text-slate-400 mt-0.5">
                    {{ Math.round(prod.calories) }} ккал | Б:{{ prod.proteins }} / Ж:{{ prod.fats }} / У:{{ prod.carbohydrates }}
                  </div>
                </td>
                <td class="p-3 sm:p-4 hidden sm:table-cell font-medium">{{ prod.calories }} ккал</td>
                <td class="p-3 sm:p-4 hidden md:table-cell text-emerald-400 font-semibold">{{ prod.proteins }}г</td>
                <td class="p-3 sm:p-4 hidden md:table-cell text-amber-400 font-semibold">{{ prod.fats }}г</td>
                <td class="p-3 sm:p-4 hidden md:table-cell text-indigo-400 font-semibold">{{ prod.carbohydrates }}г</td>
                <td class="p-3 sm:p-4 pr-4 sm:pr-6 text-right">
                  <button 
                    @click="importProduct(prod)"
                    class="px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg border border-slate-800 hover:border-brand-500 hover:bg-brand-500/10 text-brand-400 hover:text-brand-300 text-xxs sm:text-xs font-semibold transition"
                  >
                    + Добавить
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create / Edit Product Modal -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 w-full max-w-md sm:max-w-md z-50 animate-fade-in">
      <div class="w-full max-w-md p-6 rounded-2xl glass-panel border border-slate-800/80 shadow-2xl relative">
        <h3 class="text-lg font-bold text-slate-100 mb-4">
          {{ isEditing ? 'Редактировать продукт' : 'Создать/Импортировать продукт' }}
        </h3>
        
        <form @submit.prevent="saveProduct" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Название продукта</label>
            <input 
              v-model="newProduct.name" 
              type="text" 
              required 
              placeholder="например: Авокадо"
              autocorrect="on"
              autocapitalize="sentences"
              spellcheck="true"
              class="w-full px-4 py-3 rounded-xl glass-input text-sm"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Калорийность (ккал)</label>
              <input 
                v-model.number="newProduct.calories" 
                type="number" 
                step="0.1"
                required 
                placeholder="160"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Белки (г)</label>
              <input 
                v-model.number="newProduct.proteins" 
                type="number" 
                step="0.1"
                required 
                placeholder="2"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Жиры (г)</label>
              <input 
                v-model.number="newProduct.fats" 
                type="number" 
                step="0.1"
                required 
                placeholder="15"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Углеводы (г)</label>
              <input 
                v-model.number="newProduct.carbohydrates" 
                type="number" 
                step="0.1"
                required 
                placeholder="8"
                class="w-full px-4 py-3 rounded-xl glass-input text-sm"
              />
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button 
              type="button" 
              @click="closeAddDialog"
              class="px-4 py-2.5 rounded-xl border border-slate-800 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 text-sm font-semibold transition"
            >
              Отмена
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-xl gradient-btn text-white text-sm font-semibold shadow-lg shadow-brand-800/25"
            >
              {{ isEditing ? 'Обновить' : 'Сохранить' }}
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

const activeTab = ref('local')
const loading = ref(true)
const loadingExternal = ref(false)
const products = ref([])
const externalProducts = ref([])
const searchQuery = ref('')
const externalQuery = ref('')
const error = ref(null)

const showAddDialog = ref(false)
const isEditing = ref(false)
const editingProductId = ref(null)

const newProduct = ref({
  name: '',
  calories: null,
  proteins: null,
  fats: null,
  carbohydrates: null,
  is_public: true
})

const filteredProducts = computed(() => {
  if (!searchQuery.value.trim()) return products.value
  const query = searchQuery.value.toLowerCase()
  return products.value.filter(p => p.name.toLowerCase().includes(query))
})

const loadProducts = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/v1/products/')
    products.value = res.data
  } catch (err) {
    error.value = 'Не удалось загрузить локальный каталог продуктов'
  } finally {
    loading.value = false
  }
}

const searchExternal = async () => {
  if (!externalQuery.value.trim()) return
  loadingExternal.value = true
  error.value = null
  try {
    const res = await api.get(`/api/v1/products/search-external?query=${encodeURIComponent(externalQuery.value.trim())}`)
    externalProducts.value = res.data
  } catch (err) {
    error.value = 'Ошибка при поиске в базе данных продуктов. Попробуйте еще раз.'
  } finally {
    loadingExternal.value = false
  }
}

const importProduct = (extProd) => {
  isEditing.value = false
  editingProductId.value = null
  newProduct.value = {
    name: extProd.name,
    calories: extProd.calories,
    proteins: extProd.proteins,
    fats: extProd.fats,
    carbohydrates: extProd.carbohydrates,
    is_public: true
  }
  showAddDialog.value = true
}

const deleteProduct = async (productId) => {
  if (!confirm('Вы уверены, что хотите удалить этот продукт из справочника?')) return
  error.value = null
  try {
    await api.delete(`/api/v1/products/${productId}`)
    products.value = products.value.filter(p => p.id !== productId)
  } catch (err) {
    const errorMsg = err.response?.data?.detail || 'Не удалось удалить продукт. Возможно, он используется в рецептах или в вашей кладовой.'
    error.value = errorMsg
  }
}

const editProduct = (prod) => {
  isEditing.value = true
  editingProductId.value = prod.id
  newProduct.value = {
    name: prod.name,
    calories: prod.calories,
    proteins: prod.proteins,
    fats: prod.fats,
    carbohydrates: prod.carbohydrates,
    is_public: prod.is_public
  }
  showAddDialog.value = true
}

const saveProduct = async () => {
  try {
    if (isEditing.value) {
      const res = await api.put(`/api/v1/products/${editingProductId.value}`, newProduct.value)
      const index = products.value.findIndex(p => p.id === editingProductId.value)
      if (index !== -1) {
        products.value[index] = res.data
      }
      closeAddDialog()
    } else {
      const res = await api.post('/api/v1/products/', newProduct.value)
      products.value.push(res.data)
      closeAddDialog()
      activeTab.value = 'local'
      searchQuery.value = newProduct.value.name
    }
  } catch (err) {
    error.value = 'Не удалось сохранить продукт. Убедитесь, что название уникально.'
  }
}

const switchTab = (tab) => {
  activeTab.value = tab
  error.value = null
}

const closeAddDialog = () => {
  showAddDialog.value = false
  isEditing.value = false
  editingProductId.value = null
  newProduct.value = {
    name: '',
    calories: null,
    proteins: null,
    fats: null,
    carbohydrates: null,
    is_public: true
  }
}

onMounted(() => {
  loadProducts()
})
</script>
