const { test, expect } = require('@playwright/test');

test('Pantry E2E Persistence Test', async ({ page }) => {
  // Automatically accept all browser alerts/dialogs
  page.on('dialog', async dialog => {
    await dialog.accept();
  });

  const username = `user_pantry_${Date.now()}`;
  const email = `${username}@example.com`;
  const password = 'Password123!';
  const productName = `Супер Ингредиент ${username}`;

  // 1. Register a new user
  await page.goto('/register');
  await page.fill('input[placeholder="ivan_ivanov"]', username);
  await page.fill('input[placeholder="ivan@example.com"]', email);
  await page.fill('input[placeholder="••••••••"]', password);
  await page.click('button[type="submit"]');

  // Expect to reach dashboard
  await expect(page).toHaveURL(/\/dashboard/);

  // 2. Create a new product in the catalog first to ensure it exists
  await page.click('a[href="/products"]');
  await expect(page).toHaveURL(/\/products/);
  await page.click('button:has-text("Новый продукт")');
  await page.fill('input[placeholder="например: Авокадо"]', productName);
  await page.fill('input[placeholder="160"]', '100'); // calories
  await page.fill('input[placeholder="2"]', '5'); // proteins
  await page.fill('input[placeholder="15"]', '1.5'); // fats
  await page.fill('input[placeholder="8"]', '15'); // carbs
  await page.click('form button:has-text("Сохранить")');
  await page.waitForTimeout(1000); // Wait for modal close and list update
  await expect(page.locator('table')).toContainText(productName);

  // 3. Go to Pantry
  await page.click('a[href="/pantry"]');
  await expect(page).toHaveURL(/\/pantry/);

  // 4. ADD ITEM TO PANTRY
  await page.click('button:has-text("Добавить ингредиент")');
  await page.selectOption('select', { label: `${productName} (100 ккал/100г)` });
  await page.fill('input[placeholder="например: 500"]', '500');
  await page.click('form button:has-text("Добавить")');
  await page.waitForTimeout(1000);

  // Verify it exists before reload
  await expect(page.locator('table')).toContainText(productName);
  await page.screenshot({ path: 'test-results/pantry_added.png', fullPage: true });
  
  // Reload page to verify persistence
  await page.reload();
  await page.waitForTimeout(1500);
  
  // Verify it exists after reload
  const row = page.locator('tr').filter({ hasText: productName });
  await expect(row).toBeVisible();
  
  const initialWeightInput = row.locator('input[type="number"]');
  await expect(initialWeightInput).toHaveValue('500');

  // 5. EDIT ITEM WEIGHT IN PANTRY
  await initialWeightInput.fill('750');
  await initialWeightInput.blur();
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'test-results/pantry_updated.png', fullPage: true });

  // Reload page to verify persistence of edit
  await page.reload();
  await page.waitForTimeout(1500);
  
  const updatedWeightInput = page.locator('tr').filter({ hasText: productName }).locator('input[type="number"]');
  await expect(updatedWeightInput).toHaveValue('750');

  // 6. DELETE ITEM FROM PANTRY
  const deleteBtn = page.locator('tr').filter({ hasText: productName }).locator('button[title="Удалить из кладовой"]');
  await deleteBtn.click();
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'test-results/pantry_deleted.png', fullPage: true });

  // Verify it is gone before reload
  await expect(page.locator('body')).not.toContainText(productName);

  // Reload page to verify persistence of delete
  await page.reload();
  await page.waitForTimeout(1500);

  // Verify it is still gone after reload
  await expect(page.locator('body')).not.toContainText(productName);
});
