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

Locator: locator('h1.text-3xl')
Expected substring: "Привет"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for locator('h1.text-3xl')

```

```yaml
- complementary:
  - img
  - heading "To Cook List" [level=2]
  - paragraph: Кулинарный навигатор
  - navigation:
    - link "Панель управления":
      - /url: /dashboard
      - img
      - text: Панель управления
    - link "Моя кладовая":
      - /url: /pantry
      - img
      - text: Моя кладовая
    - link "Справочник КБЖУ":
      - /url: /products
      - img
      - text: Справочник КБЖУ
    - link "Рецепты":
      - /url: /recipes
      - img
      - text: Рецепты
    - link "Планировщик":
      - /url: /menu
      - img
      - text: Планировщик
    - link "Социальная панель":
      - /url: /social
      - img
      - text: Социальная панель
  - text: U
  - paragraph: user_1783167458389
  - paragraph: В сети
  - button "Выйти":
    - img
    - text: Выйти
- main:
  - heading "Панель управления" [level=1]
  - text: Подключено к API
  - heading "Привет, user_1783167458389!" [level=1]
  - paragraph: Вот твой кулинарный обзор на сегодня.
  - link "Обзор рецептов":
    - /url: /recipes
  - link "Планировать меню":
    - /url: /menu
  - img
  - paragraph: Моя кладовая
  - heading "0" [level=3]
  - paragraph: Ингредиентов в наличии
  - img
  - paragraph: Всего рецептов
  - heading "1" [level=3]
  - paragraph: Доступно кулинарных карт
  - img
  - paragraph: Блюда на сегодня
  - heading "0" [level=3]
  - paragraph: Запланировано на сегодня
  - img
  - paragraph: Социальная активность
  - heading "0" [level=3]
  - paragraph: Ожидает запросов
  - heading "Расписание на сегодня" [level=2]:
    - img
    - text: Расписание на сегодня
  - img
  - paragraph: На сегодня нет запланированных блюд.
  - link "Запланировать блюдо →":
    - /url: /menu
  - heading "Входящие запросы" [level=2]:
    - img
    - text: Входящие запросы
  - paragraph: Нет входящих запросов от других пользователей.
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
> 25  |   await expect(page.locator('h1.text-3xl')).toContainText('Привет');
      |                                             ^ Error: expect(locator).toContainText(expected) failed
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