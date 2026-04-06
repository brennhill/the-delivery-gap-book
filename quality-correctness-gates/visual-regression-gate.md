# Visual Regression Gate

AI coding agents generate UI code with high confidence and zero visual awareness. They cannot see what a component looks like after they change it. A unit test confirms the button calls the right handler. A visual regression test confirms the button is still visible, properly aligned, and not occluded by a modal the agent didn't know about.

This is not optional for teams where agents touch frontend code. Without it, you will ship styling regressions, layout breaks, and rendering bugs that no linter, type checker, or unit test can catch.

---

## The Problem

AI agents modify CSS, component structure, and layout logic based on textual understanding of the code. They have no rendering engine. Common failures:

- **Z-index collisions** — agent adds a dropdown, doesn't know it renders behind a sticky header
- **Responsive breakage** — agent fixes desktop layout, breaks mobile (never checked)
- **Styling side effects** — agent changes a shared class, affects 12 other components
- **Missing visual states** — agent implements the happy path, loading/error/empty states render broken
- **Whitespace and alignment drift** — technically correct DOM, visually wrong spacing

These all pass CI. They all fail the user's eyes.

---

## Tools

### Playwright Screenshot Assertions (Free, open source)

Playwright's built-in `toHaveScreenshot()` captures baseline screenshots and diffs against them on every test run. No external service required. Runs in CI.

```typescript
import { test, expect } from '@playwright/test';

test('checkout page visual regression', async ({ page }) => {
  await page.goto('/checkout');
  await expect(page).toHaveScreenshot('checkout.png', {
    maxDiffPixelRatio: 0.01,  // 1% pixel diff threshold
  });
});

test('checkout page — mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/checkout');
  await expect(page).toHaveScreenshot('checkout-mobile.png');
});
```

**Setup:**
```bash
npx playwright install --with-deps chromium
npx playwright test --update-snapshots  # Generate initial baselines
```

**CI integration (GitHub Actions):**
```yaml
- name: Visual regression tests
  run: npx playwright test --project=visual
- name: Upload diff artifacts
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: visual-diffs
    path: test-results/
```

When a visual test fails, Playwright generates three images: expected, actual, and diff. The diff highlights every changed pixel. Upload these as CI artifacts so reviewers can see exactly what changed.

### Chromatic (SaaS, Storybook integration)

If you use Storybook, Chromatic captures every story as a screenshot and diffs against the baseline on every PR. It handles cross-browser rendering, responsive viewports, and provides a review UI for approving intentional changes.

```bash
npx chromatic --project-token=$CHROMATIC_TOKEN
```

Best for teams with an existing Storybook setup. Catches component-level regressions without writing explicit visual tests.

### Percy (SaaS, framework-agnostic)

Percy integrates with Playwright, Cypress, Selenium, and others. It renders pages in multiple browsers and viewports, diffs against baselines, and provides a review dashboard.

```typescript
// With Playwright
import percySnapshot from '@percy/playwright';

test('homepage visual', async ({ page }) => {
  await page.goto('/');
  await percySnapshot(page, 'Homepage');
});
```

Best for teams that need cross-browser visual coverage without maintaining their own screenshot infrastructure.

---

## What to Cover

Prioritize pages and states that agents are most likely to break:

1. **Critical user flows** — checkout, login, dashboard, onboarding
2. **Responsive breakpoints** — at minimum: mobile (375px), tablet (768px), desktop (1280px)
3. **Component states** — loading, error, empty, populated, disabled
4. **Dark mode / theme variants** — if applicable

You don't need 100% visual coverage. You need coverage on the paths agents are most likely to touch and least likely to manually verify.

---

## Integration as a Gate

Visual regression tests should block merge, not just report. Configure them the same way you configure unit tests — as a required CI check on every PR.

For agent-generated PRs specifically:

- Run visual tests as part of the standard CI pipeline (agents don't get to skip them)
- If visual diffs are detected, require human approval of the visual changes before merge
- Store baseline screenshots in version control (not a remote service) so the agent can update them when the change is intentional

The agent can update baselines with `npx playwright test --update-snapshots`, but the diff should still be visible in the PR for human review.

---

## Key Principle

Unit tests verify behavior. Type checks verify structure. Visual regression tests verify *what the user actually sees*. For AI-generated UI code, this is the gate that catches what every other gate misses.
