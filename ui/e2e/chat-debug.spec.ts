import { test, expect } from '@playwright/test';

test('debug chat flow', async ({ page }) => {
  // Go to chat
  await page.goto('http://localhost:3000');
  await page.waitForLoadState('networkidle');

  // Screenshot initial state
  await page.screenshot({ path: '/tmp/debug-1-initial.png' });

  // Find and fill chat input
  const chatInput = page.locator('textarea').first();
  await expect(chatInput).toBeVisible({ timeout: 10000 });
  await chatInput.click();
  await chatInput.fill('Hello');

  await page.screenshot({ path: '/tmp/debug-2-typed.png' });

  // Find send button (look for button near the textarea)
  const sendButton = page.locator('button').last();
  console.log('Send button found:', await sendButton.isVisible());

  // Click send
  await sendButton.click();

  // Wait and take screenshots at intervals
  await page.waitForTimeout(2000);
  await page.screenshot({ path: '/tmp/debug-3-after2s.png' });

  await page.waitForTimeout(5000);
  await page.screenshot({ path: '/tmp/debug-4-after7s.png' });

  await page.waitForTimeout(10000);
  await page.screenshot({ path: '/tmp/debug-5-after17s.png' });

  // Get page content
  const content = await page.content();
  console.log('Page has content length:', content.length);

  // Check for any error messages
  const errorText = await page.locator('text=/error|failed|timeout/i').count();
  console.log('Error elements found:', errorText);
});
