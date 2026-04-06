import { test, expect } from '@playwright/test';

test('debug streaming and intermediate steps', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.waitForLoadState('networkidle');

  // Take initial screenshot
  await page.screenshot({ path: '/tmp/stream-1-initial.png' });

  // Find and fill chat input
  const chatInput = page.locator('textarea').first();
  await expect(chatInput).toBeVisible({ timeout: 10000 });
  await chatInput.click();
  await chatInput.fill('List files in the current directory');

  // Click send button
  const sendButton = page.locator('button').last();
  await sendButton.click();

  // Take screenshots during streaming
  for (let i = 2; i <= 10; i++) {
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `/tmp/stream-${i}-after${(i-1)*2}s.png` });
  }

  // Log any console errors
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('Browser error:', msg.text());
    }
  });

  // Check for intermediate steps elements
  const intermediateSteps = await page.locator('[class*="intermediate"]').count();
  console.log('Intermediate step elements found:', intermediateSteps);

  // Check for any expandable/collapsible sections
  const expandables = await page.locator('details, [class*="expand"], [class*="collapse"]').count();
  console.log('Expandable elements found:', expandables);
});
