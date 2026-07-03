const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  let testUsername = '';
  let testPassword = '';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--username' && args[i+1]) {
      testUsername = args[i+1];
    }
    if (args[i] === '--password' && args[i+1]) {
      testPassword = args[i+1];
    }
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  const page = await context.newPage();
  
  const logs = [];
  page.on('console', msg => {
    logs.push(`[${msg.type()}] ${msg.text()}`);
  });
  page.on('pageerror', err => {
    logs.push(`[ERROR] ${err.message}`);
  });

  const screenshotsDir = path.join(__dirname, 'test-screenshots');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir);
  }

  console.log('Starting UI testing script...');
  
  try {
    if (testUsername && testPassword) {
      console.log(`Logging in as existing user: ${testUsername}...`);
      await page.goto('http://127.0.0.1:5173/login');
      // Wait for login inputs
      await page.waitForSelector('input[type="text"]');
      await page.fill('input[type="text"]', testUsername);
      await page.fill('input[type="password"]', testPassword);
      await page.click('button[type="submit"]');
      await page.waitForTimeout(2000);
    } else {
      testUsername = `test_ui_${Date.now()}`;
      testPassword = 'Password123!';
      console.log(`Registering new test user: ${testUsername}...`);
      await page.goto('http://127.0.0.1:5173/register');
      await page.waitForSelector('input[placeholder="ivan_ivanov"]');
      await page.fill('input[placeholder="ivan_ivanov"]', testUsername);
      await page.fill('input[placeholder="ivan@example.com"]', `${testUsername}@example.com`);
      await page.fill('input[placeholder="••••••••"]', testPassword);
      await page.click('button[type="submit"]');
      await page.waitForTimeout(2000);
    }

    const steps = [
      { name: '1_dashboard', url: '/dashboard', label: 'Панель управления' },
      { name: '2_pantry', url: '/pantry', label: 'Моя кладовая' },
      { name: '3_products', url: '/products', label: 'Справочник КБЖУ' },
      { name: '4_recipes', url: '/recipes', label: 'Рецепты' },
      { name: '5_menu', url: '/menu', label: 'Планировщик' },
      { name: '6_social', url: '/social', label: 'Социальная панель' }
    ];

    const results = [];

    for (const step of steps) {
      console.log(`Navigating to ${step.label} (${step.url})...`);
      try {
        await page.goto(`http://127.0.0.1:5173${step.url}`);
        await page.waitForTimeout(1500);
        
        // Take screenshot
        const screenshotPath = path.join(screenshotsDir, `${step.name}.png`);
        await page.screenshot({ path: screenshotPath });
        
        const currentUrl = page.url();
        
        results.push({
          step: step.label,
          status: currentUrl.includes(step.url) ? 'Успешно' : 'Ошибка перенаправления',
          url: currentUrl,
          screenshot: `${step.name}.png`
        });
      } catch (err) {
        results.push({
          step: step.label,
          status: `Ошибка: ${err.message}`,
          url: 'N/A',
          screenshot: ''
        });
      }
    }

    // Generate markdown report
    let reportMd = `# Отчет о тестировании UI от ${new Date().toLocaleString()}\n\n`;
    reportMd += `Пользователь: **${testUsername}**\n\n`;
    reportMd += `| Раздел | Статус | URL | Скриншот |\n`;
    reportMd += `| --- | --- | --- | --- |\n`;
    for (const res of results) {
      reportMd += `| ${res.step} | ${res.status} | ${res.url} | [${res.screenshot}](./test-screenshots/${res.screenshot}) |\n`;
    }
    
    reportMd += `\n## Логи консоли браузера:\n\`\`\`\n`;
    reportMd += logs.join('\n') || 'Логов нет';
    reportMd += `\n\`\`\`\n`;

    fs.writeFileSync(path.join(__dirname, 'ui_test_report.md'), reportMd);
    console.log('UI Testing completed! Report generated: ui_test_report.md');
    
  } catch (err) {
    console.error(`Global test failure: ${err.message}`);
  } finally {
    await browser.close();
  }
})();
