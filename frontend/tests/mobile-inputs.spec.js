const { test, expect } = require('@playwright/test');

test('Mobile Inputs and Autocomplete Configuration Test', async ({ page }) => {
  // Go to login page and check input attributes for keyboard and autofill
  await page.goto('/login');
  const loginUsername = page.locator('input[placeholder="ivan_ivanov"]');
  const loginPassword = page.locator('input[placeholder="••••••••"]');
  
  await expect(loginUsername).toHaveAttribute('autocomplete', 'username');
  await expect(loginUsername).toHaveAttribute('autocorrect', 'off');
  await expect(loginUsername).toHaveAttribute('spellcheck', 'false');
  await expect(loginPassword).toHaveAttribute('autocomplete', 'current-password');

  // Go to register page and check inputs
  await page.goto('/register');
  const registerUsername = page.locator('input[placeholder="ivan_ivanov"]');
  const registerEmail = page.locator('input[placeholder="ivan@example.com"]');
  const registerPassword = page.locator('input[placeholder="••••••••"]');

  await expect(registerUsername).toHaveAttribute('autocomplete', 'username');
  await expect(registerEmail).toHaveAttribute('autocomplete', 'email');
  await expect(registerPassword).toHaveAttribute('autocomplete', 'new-password');

  // Go to products page and check search inputs for T9 auto-correct features
  // We need to bypass login first using a dummy session or directly filling the login form
  await page.goto('/login');
  await loginUsername.fill('test_user_keyb');
  await loginPassword.fill('password123');
  
  // Register if not exists (E2E user flow handles creation, we just verify attributes)
  await page.goto('/register');
  const regUser = `user_k_${Date.now()}`;
  await page.fill('input[placeholder="ivan_ivanov"]', regUser);
  await page.fill('input[placeholder="ivan@example.com"]', `${regUser}@example.com`);
  await page.fill('input[placeholder="••••••••"]', 'Password123!');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/dashboard/);

  // Navigate to Products and inspect the input elements
  await page.goto('/products');
  await page.click('button:has-text("Поиск в Интернете")');
  const searchInput = page.locator('input[placeholder*="творог"]');
  await expect(searchInput).toHaveAttribute('autocorrect', 'on');
  await expect(searchInput).toHaveAttribute('spellcheck', 'true');
  await expect(searchInput).toHaveAttribute('autocapitalize', 'sentences');

  // Open add dialog and check name input
  await page.click('button:has-text("Новый продукт")');
  const addNameInput = page.locator('input[placeholder="например: Авокадо"]');
  await expect(addNameInput).toHaveAttribute('autocorrect', 'on');
  await expect(addNameInput).toHaveAttribute('spellcheck', 'true');
  await expect(addNameInput).toHaveAttribute('autocapitalize', 'sentences');
});
