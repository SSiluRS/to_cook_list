# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: culinary.spec.js >> Culinary Navigator E2E User Flow
- Location: tests\culinary.spec.js:3:1

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('h1')
Expected substring: "Привет"
Error: strict mode violation: locator('h1') resolved to 2 elements:
    1) <h1 class="text-base lg:text-lg font-bold bg-gradient-to-r from-slate-200 to-slate-400 bg-clip-text text-transparent truncate">Панель управления</h1> aka getByRole('heading', { name: 'Панель управления' })
    2) <h1 class="text-xl sm:text-3xl font-extrabold tracking-tight bg-gradient-to-r from-slate-50 to-slate-300 bg-clip-text text-transparent"> Привет, user_1783167489819! </h1> aka getByRole('heading', { name: 'Привет, user_1783167489819!' })

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for locator('h1')
    3 × locator resolved to <h1 class="text-base lg:text-lg font-bold bg-gradient-to-r from-slate-200 to-slate-400 bg-clip-text text-transparent truncate">Панель управления</h1>
      - unexpected value "Панель управления"

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - complementary [ref=e4]:
    - generic [ref=e5]:
      - generic [ref=e6]:
        - img [ref=e8]
        - generic [ref=e10]:
          - heading "To Cook List" [level=2] [ref=e11]
          - paragraph [ref=e12]: Кулинарный навигатор
      - navigation [ref=e13]:
        - link "Панель управления" [ref=e14] [cursor=pointer]:
          - /url: /dashboard
          - img [ref=e15]
          - text: Панель управления
        - link "Моя кладовая" [ref=e17] [cursor=pointer]:
          - /url: /pantry
          - img [ref=e18]
          - text: Моя кладовая
        - link "Справочник КБЖУ" [ref=e20] [cursor=pointer]:
          - /url: /products
          - img [ref=e21]
          - text: Справочник КБЖУ
        - link "Рецепты" [ref=e23] [cursor=pointer]:
          - /url: /recipes
          - img [ref=e24]
          - text: Рецепты
        - link "Планировщик" [ref=e26] [cursor=pointer]:
          - /url: /menu
          - img [ref=e27]
          - text: Планировщик
        - link "Социальная панель" [ref=e29] [cursor=pointer]:
          - /url: /social
          - img [ref=e30]
          - text: Социальная панель
    - generic [ref=e32]:
      - generic [ref=e33]:
        - generic [ref=e34]: U
        - generic [ref=e35]:
          - paragraph [ref=e36]: user_1783167489819
          - paragraph [ref=e37]: В сети
      - button "Выйти" [ref=e38] [cursor=pointer]:
        - img [ref=e39]
        - text: Выйти
  - main [ref=e41]:
    - generic [ref=e42]:
      - heading "Панель управления" [level=1] [ref=e43]
      - generic [ref=e46]: Подключено к API
    - generic [ref=e48]:
      - generic [ref=e49]:
        - generic [ref=e50]:
          - heading "Привет, user_1783167489819!" [level=1] [ref=e51]
          - paragraph [ref=e52]: Вот твой кулинарный обзор на сегодня.
        - generic [ref=e53]:
          - link "Обзор рецептов" [ref=e54] [cursor=pointer]:
            - /url: /recipes
          - link "Планировать меню" [ref=e55] [cursor=pointer]:
            - /url: /menu
      - generic [ref=e56]:
        - generic [ref=e57]:
          - img [ref=e59]
          - paragraph [ref=e61]: Моя кладовая
          - heading "0" [level=3] [ref=e62]
          - paragraph [ref=e63]: Ингредиентов в наличии
        - generic [ref=e64]:
          - img [ref=e66]
          - paragraph [ref=e68]: Всего рецептов
          - heading "1" [level=3] [ref=e69]
          - paragraph [ref=e70]: Доступно кулинарных карт
        - generic [ref=e71]:
          - img [ref=e73]
          - paragraph [ref=e75]: Блюда на сегодня
          - heading "0" [level=3] [ref=e76]
          - paragraph [ref=e77]: Запланировано на сегодня
        - generic [ref=e78]:
          - img [ref=e80]
          - paragraph [ref=e82]: Социальная активность
          - heading "0" [level=3] [ref=e83]
          - paragraph [ref=e84]: Ожидает запросов
      - generic [ref=e85]:
        - generic [ref=e87]:
          - heading "Расписание на сегодня" [level=2] [ref=e88]:
            - img [ref=e89]
            - text: Расписание на сегодня
          - generic [ref=e91]:
            - img [ref=e92]
            - paragraph [ref=e94]: На сегодня нет запланированных блюд.
            - link "Запланировать блюдо →" [ref=e95] [cursor=pointer]:
              - /url: /menu
        - generic [ref=e97]:
          - heading "Входящие запросы" [level=2] [ref=e98]:
            - img [ref=e99]
            - text: Входящие запросы
          - paragraph [ref=e102]: Нет входящих запросов от других пользователей.
```

# Test source

```ts
  1   | const { test, expect } = require('@playwright/test');
  2   | 
  3   | test('Culinary Navigator E2E User Flow', async ({ page }) => {
  4   |   // Automatically accept all browser alerts/dialogs
  5   |   page.on('dialog', async dialog => {
  6   |     await dialog.accept();
  7   |   });
  8   | 
  9   |   const username = `user_${Date.now()}`;
  10  |   const email = `${username}@example.com`;
  11  |   const password = 'Password123!';
  12  |   
  13  |   const productName = `Тестовый Банан ${username}`;
  14  |   const recipeName = `Банановый Десерт ${username}`;
  15  | 
  16  |   // 1. Go to register page
  17  |   await page.goto('/register');
  18  |   await page.fill('input[placeholder="ivan_ivanov"]', username);
  19  |   await page.fill('input[placeholder="ivan@example.com"]', email);
  20  |   await page.fill('input[placeholder="••••••••"]', password);
  21  |   await page.click('button[type="submit"]');
  22  | 
  23  |   // 2. Expect to reach dashboard
  24  |   await expect(page).toHaveURL(/\/dashboard/);
> 25  |   await expect(page.locator('h1')).toContainText('Привет');
      |                                    ^ Error: expect(locator).toContainText(expected) failed
  26  | 
  27  |   // 3. Create a new product in the catalog
  28  |   await page.click('a[href="/products"]');
  29  |   await expect(page).toHaveURL(/\/products/);
  30  |   await page.click('button:has-text("Новый продукт")');
  31  |   await page.fill('input[placeholder="например: Авокадо"]', productName);
  32  |   await page.fill('input[placeholder="160"]', '90');
  33  |   await page.fill('input[placeholder="2"]', '1.2');
  34  |   await page.fill('input[placeholder="15"]', '0.2');
  35  |   await page.fill('input[placeholder="8"]', '22');
  36  |   await page.click('form button:has-text("Сохранить")');
  37  |   await page.waitForTimeout(1000); // Wait for modal close and list update
  38  |   await expect(page.locator('table')).toContainText(productName);
  39  | 
  40  |   // Edit the newly created product
  41  |   await page.click(`tr:has-text("${productName}") button:has-text("Редактировать")`);
  42  |   await page.waitForSelector('h3:has-text("Редактировать продукт")');
  43  |   await page.fill('input[placeholder="160"]', '95');
  44  |   await page.click('form button:has-text("Обновить")');
  45  |   await page.waitForTimeout(1000);
  46  |   await expect(page.locator('table')).toContainText('95 ккал');
  47  | 
  48  |   // 3b. Test searching product from Internet and importing it
  49  |   await page.route('**/api/v1/products/search-external*', async route => {
  50  |     await route.fulfill({
  51  |       status: 200,
  52  |       contentType: 'application/json',
  53  |       body: JSON.stringify([
  54  |         {
  55  |           name: 'Филе курица',
  56  |           calories: 110.0,
  57  |           proteins: 23.0,
  58  |           fats: 1.2,
  59  |           carbohydrates: 0.0
  60  |         }
  61  |       ])
  62  |     });
  63  |   });
  64  | 
  65  |   await page.click('button:has-text("Поиск в Интернете")');
  66  |   await page.fill('input[placeholder*="творог"]', 'филе курица');
  67  |   await page.click('form button:has-text("Найти")');
  68  |   await expect(page.locator('table')).toContainText('курица', { timeout: 10000 });
  69  |   await page.click('table button:has-text("+ Добавить")');
  70  |   await page.waitForSelector('h3:has-text("Создать/Импортировать продукт")');
  71  |   const importedName = `Импорт Курица ${Date.now()}`;
  72  |   await page.fill('input[placeholder="например: Авокадо"]', importedName);
  73  |   await page.click('form button:has-text("Сохранить")');
  74  |   await page.waitForTimeout(1000);
  75  |   await expect(page.locator('table')).toContainText(importedName);
  76  | 
  77  |   // 4. Add product to Pantry
  78  |   await page.click('a[href="/pantry"]');
  79  |   await expect(page).toHaveURL(/\/pantry/);
  80  |   await page.click('button:has-text("Добавить ингредиент")');
  81  |   await page.selectOption('select', { label: `${productName} (90 ккал/100г)` });
  82  |   await page.fill('input[placeholder="например: 500"]', '300');
  83  |   await page.click('form button:has-text("Добавить")');
  84  |   await page.waitForTimeout(1000);
  85  |   await expect(page.locator('table')).toContainText(productName);
  86  | 
  87  |   // 5. Create a Recipe using this product
  88  |   await page.click('a[href="/recipes"]');
  89  |   await expect(page).toHaveURL(/\/recipes/);
  90  |   await page.click('button:has-text("Создать рецепт")');
  91  |   await page.fill('input[placeholder="например: Авокадо Тост"]', recipeName);
  92  |   await page.fill('input[placeholder="например: Простой и полезный завтрак"]', 'Вкусный перекус');
  93  |   await page.fill('textarea[placeholder*="хлеб"]', '1. Очистить банан. 2. Нарезать.');
  94  |   await page.selectOption('select', { label: `${productName} (90 ккал/100г)` });
  95  |   await page.fill('input[placeholder="Вес (г)"]', '150');
  96  |   await page.click('form button:has-text("Сохранить")');
  97  |   await page.waitForTimeout(1000);
  98  |   await expect(page.locator('.grid')).toContainText(recipeName);
  99  | 
  100 |   // 6. Go to Recipe details and verify smart matching
  101 |   await page.click(`h3:has-text("${recipeName}")`);
  102 |   await expect(page).toHaveURL(/\/recipes\/[a-f0-9-]+/);
  103 |   await expect(page.getByText('У вас есть все ингредиенты! Можно готовить.')).toBeVisible();
  104 | 
  105 |   // 7. Schedule the recipe for today
  106 |   await page.click('button:has-text("Запланировать")');
  107 |   const todayStr = new Date().toISOString().split('T')[0];
  108 |   await page.fill('input[type="date"]', todayStr);
  109 |   await page.selectOption('select', 'Breakfast');
  110 |   await page.click('button[type="submit"]');
  111 |   await page.waitForTimeout(1000);
  112 | 
  113 |   // 8. Go to Dashboard and verify the meal is scheduled
  114 |   await page.click('a[href="/dashboard"]');
  115 |   await expect(page).toHaveURL(/\/dashboard/);
  116 |   await expect(page.getByText(recipeName)).toBeVisible();
  117 | 
  118 |   // 9. Try deleting the product (should fail because it is in use)
  119 |   await page.click('a[href="/products"]');
  120 |   await expect(page).toHaveURL(/\/products/);
  121 |   page.once('dialog', dialog => dialog.accept());
  122 |   await page.click(`tr:has-text("${productName}") button:has-text("Удалить")`);
  123 |   await page.waitForTimeout(1000);
  124 |   await expect(page.locator('.bg-rose-500\\/10')).toContainText('используется в кладовой или в рецептах');
  125 | });
```