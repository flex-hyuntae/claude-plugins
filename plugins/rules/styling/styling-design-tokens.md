---
title: 디자인 토큰 활용
impact: HIGH
impactDescription: 일관된 디자인 시스템 유지
tags: css, design-tokens, vanilla-extract, styling
---

## 디자인 토큰 활용

하드코딩된 색상/크기 값 대신 디자인 시스템 토큰(vars)을 사용한다.

**Incorrect (하드코딩 값):**

```typescript
// style.css.ts
import { style } from '@vanilla-extract/css';

export const container = style({
  color: '#333333',
  fontSize: '14px',
  padding: '8px 16px',
  borderRadius: '4px',
  backgroundColor: '#ffffff',
});
```

**Correct (디자인 토큰 사용):**

```typescript
// style.css.ts
import { style } from '@vanilla-extract/css';
import { vars } from '@flex-design-system/vars';

export const container = style({
  color: vars.color.text.primary,
  fontSize: vars.typography.body2.fontSize,
  padding: `${vars.spacing[2]} ${vars.spacing[4]}`,
  borderRadius: vars.radius.sm,
  backgroundColor: vars.color.surface.default,
});
```

**sprinkles 활용:**

```typescript
// style.css.ts
import { sprinkles } from '@flex-design-system/sprinkles';

export const container = sprinkles({
  color: 'text-primary',
  fontSize: 'body2',
  padding: 'md',
  borderRadius: 'sm',
});
```
