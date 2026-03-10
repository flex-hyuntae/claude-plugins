---
title: vanilla-extract 패턴
impact: HIGH
impactDescription: 제로 런타임 CSS, 타입 안전한 스타일링
tags: css, vanilla-extract, styling, performance
---

## vanilla-extract 패턴

스타일은 `style.css.ts` 파일에 분리하고, `style()`, `styleVariants()`, `recipe()`를 적절히 사용한다.

**Incorrect (인라인 스타일 / 런타임 CSS-in-JS):**

```tsx
// 컴포넌트 내 인라인 스타일
function Card({ variant }: { variant: "primary" | "secondary" }) {
  return (
    <div
      style={{
        padding: "16px",
        backgroundColor: variant === "primary" ? "#0066ff" : "#gray",
      }}
    >
      ...
    </div>
  );
}
```

**Correct (vanilla-extract 분리):**

```typescript
// style.css.ts
import { style, styleVariants } from "@vanilla-extract/css";

export const card = style({
  padding: 16,
});

export const cardVariant = styleVariants({
  primary: { backgroundColor: "#0066ff" },
  secondary: { backgroundColor: "#gray" },
});
```

```tsx
// index.tsx
import { card, cardVariant } from "./style.css";

function Card({ variant }: { variant: "primary" | "secondary" }) {
  return <div className={`${card} ${cardVariant[variant]}`}>...</div>;
}
```

**동적 스타일이 필요한 경우 (assignInlineVars):**

```typescript
// style.css.ts
import { createVar, style } from "@vanilla-extract/css";

export const progressVar = createVar();

export const progressBar = style({
  width: progressVar,
});
```

```tsx
// index.tsx
import { assignInlineVars } from "@vanilla-extract/dynamic";
import { progressBar, progressVar } from "./style.css";

function ProgressBar({ value }: { value: number }) {
  return (
    <div
      className={progressBar}
      style={assignInlineVars({ [progressVar]: `${value}%` })}
    />
  );
}
```
