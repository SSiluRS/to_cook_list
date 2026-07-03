const { test, expect } = require('@playwright/test');

test('Culinary Navigator E2E User Flow', async ({ page }) => {
  // Automatically accept all browser alerts/dialogs
  page.on('dialog', async dialog => {
    await dialog.accept();
  });

  const username = `user_${Date.now()}`;
  const email = `${username}@example.com`;
  const password = 'Password123!';
  
  const productName = `Тестовый Банан ${username}`;
  const recipeName = `Банановый Десерт ${username}`;

  // 1. Go to register page
  await page.goto('/register');
  await page.fill('input[placeholder="ivan_ivanov"]', username);
  await page.fill('input[placeholder="ivan@example.com"]', email);
  await page.fill('input[placeholder="••••••••"]', password);
  await page.click('button[type="submit"]');

  // 2. Expect to reach dashboard
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.locator('h1.text-3xl')).toContainText('Привет');

  // 3. Create a new product in the catalog
  await page.click('a[href="/products"]');
  await expect(page).toHaveURL(/\/products/);
  await page.click('button:has-text("Новый продукт")');
  await page.fill('input[placeholder="например: Авокадо"]', productName);
  await page.fill('input[placeholder="160"]', '90');
  await page.fill('input[placeholder="2"]', '1.2');
  await page.fill('input[placeholder="15"]', '0.2');
  await page.fill('input[placeholder="8"]', '22');
  await page.click('form button:has-text("Сохранить")');
  await page.waitForTimeout(1000); // Wait for modal close and list update
  await expect(page.locator('table')).toContainText(productName);

  // 4. Add product to Pantry
  await page.click('a[href="/pantry"]');
  await expect(page).toHaveURL(/\/pantry/);
  await page.click('button:has-text("Добавить ингредиент")');
  await page.selectOption('select', { label: `${productName} (90 ккал/100г)` });
  await page.fill('input[placeholder="например: 500"]', '300');
  await page.click('form button:has-text("Добавить")');
  await page.waitForTimeout(1000);
  await expect(page.locator('table')).toContainText(productName);

  // 5. Create a Recipe using this product
  await page.click('a[href="/recipes"]');
  await expect(page).toHaveURL(/\/recipes/);
  await page.click('button:has-text("Создать рецепт")');
  await page.fill('input[placeholder="например: Авокадо Тост"]', recipeName);
  await page.fill('input[placeholder="например: Простой и полезный завтрак"]', 'Вкусный перекус');
  await page.fill('textarea[placeholder*="хлеб"]', '1. Очистить банан. 2. Нарезать.');
  await page.selectOption('select', { label: `${productName} (90 ккал/100г)` });
  await page.fill('input[placeholder="Вес (г)"]', '150');
  await page.click('form button:has-text("Сохранить")');
  await page.waitForTimeout(1000);
  await expect(page.locator('.grid')).toContainText(recipeName);

  // 6. Go to Recipe details and verify smart matching
  await page.click(`h3:has-text("${recipeName}")`);
  await expect(page).toHaveURL(/\/recipes\/[a-f0-9-]+/);
  await expect(page.getByText('У вас есть все ингредиенты! Можно готовить.')).toBeVisible();

  // 7. Schedule the recipe for today
  await page.click('button:has-text("Запланировать")');
  const todayStr = new Date().toISOString().split('T')[0];
  await page.fill('input[type="date"]', todayStr);
  await page.selectOption('select', 'Breakfast');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(1000);

  // 8. Go to Dashboard and verify the meal is scheduled
  await page.click('a[href="/dashboard"]');
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByText(recipeName)).toBeVisible();
});
