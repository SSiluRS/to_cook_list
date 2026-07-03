# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: pantry.spec.js >> Pantry E2E Persistence Test
- Location: tests\pantry.spec.js:3:1

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.goto: Test timeout of 30000ms exceeded.
Call log:
  - navigating to "http://127.0.0.1:5173/register", waiting until "load"

```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | test('Pantry E2E Persistence Test', async ({ page }) => {
  4  |   // Automatically accept all browser alerts/dialogs
  5  |   page.on('dialog', async dialog => {
  6  |     await dialog.accept();
  7  |   });
  8  | 
  9  |   const username = `user_pantry_${Date.now()}`;
  10 |   const email = `${username}@example.com`;
  11 |   const password = 'Password123!';
  12 |   const productName = `Супер Ингредиент ${username}`;
  13 | 
  14 |   // 1. Register a new user
> 15 |   await page.goto('/register');
     |              ^ Error: page.goto: Test timeout of 30000ms exceeded.
  16 |   await page.fill('input[placeholder="ivan_ivanov"]', username);
  17 |   await page.fill('input[placeholder="ivan@example.com"]', email);
  18 |   await page.fill('input[placeholder="••••••••"]', password);
  19 |   await page.click('button[type="submit"]');
  20 | 
  21 |   // Expect to reach dashboard
  22 |   await expect(page).toHaveURL(/\/dashboard/);
  23 | 
  24 |   // 2. Create a new product in the catalog first to ensure it exists
  25 |   await page.click('a[href="/products"]');
  26 |   await expect(page).toHaveURL(/\/products/);
  27 |   await page.click('button:has-text("Новый продукт")');
  28 |   await page.fill('input[placeholder="например: Авокадо"]', productName);
  29 |   await page.fill('input[placeholder="160"]', '100'); // calories
  30 |   await page.fill('input[placeholder="2"]', '5'); // proteins
  31 |   await page.fill('input[placeholder="15"]', '1.5'); // fats
  32 |   await page.fill('input[placeholder="8"]', '15'); // carbs
  33 |   await page.click('form button:has-text("Сохранить")');
  34 |   await page.waitForTimeout(1000); // Wait for modal close and list update
  35 |   await expect(page.locator('table')).toContainText(productName);
  36 | 
  37 |   // 3. Go to Pantry
  38 |   await page.click('a[href="/pantry"]');
  39 |   await expect(page).toHaveURL(/\/pantry/);
  40 | 
  41 |   // 4. ADD ITEM TO PANTRY
  42 |   await page.click('button:has-text("Добавить ингредиент")');
  43 |   await page.selectOption('select', { label: `${productName} (100 ккал/100г)` });
  44 |   await page.fill('input[placeholder="например: 500"]', '500');
  45 |   await page.click('form button:has-text("Добавить")');
  46 |   await page.waitForTimeout(1000);
  47 | 
  48 |   // Verify it exists before reload
  49 |   await expect(page.locator('table')).toContainText(productName);
  50 |   
  51 |   // Reload page to verify persistence
  52 |   await page.reload();
  53 |   await page.waitForTimeout(1500);
  54 |   
  55 |   // Verify it exists after reload
  56 |   const row = page.locator('tr').filter({ hasText: productName });
  57 |   await expect(row).toBeVisible();
  58 |   
  59 |   const initialWeightInput = row.locator('input[type="number"]');
  60 |   await expect(initialWeightInput).toHaveValue('500');
  61 | 
  62 |   // 5. EDIT ITEM WEIGHT IN PANTRY
  63 |   await initialWeightInput.fill('750');
  64 |   await initialWeightInput.blur();
  65 |   await page.waitForTimeout(1500);
  66 | 
  67 |   // Reload page to verify persistence of edit
  68 |   await page.reload();
  69 |   await page.waitForTimeout(1500);
  70 |   
  71 |   const updatedWeightInput = page.locator('tr').filter({ hasText: productName }).locator('input[type="number"]');
  72 |   await expect(updatedWeightInput).toHaveValue('750');
  73 | 
  74 |   // 6. DELETE ITEM FROM PANTRY
  75 |   const deleteBtn = page.locator('tr').filter({ hasText: productName }).locator('button[title="Удалить из кладовой"]');
  76 |   await deleteBtn.click();
  77 |   await page.waitForTimeout(1500);
  78 | 
  79 |   // Verify it is gone before reload
  80 |   await expect(page.locator('body')).not.toContainText(productName);
  81 | 
  82 |   // Reload page to verify persistence of delete
  83 |   await page.reload();
  84 |   await page.waitForTimeout(1500);
  85 | 
  86 |   // Verify it is still gone after reload
  87 |   await expect(page.locator('body')).not.toContainText(productName);
  88 | });
  89 | 
```