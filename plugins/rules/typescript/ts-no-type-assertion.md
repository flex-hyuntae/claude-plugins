---
title: Type Assertion 금지
impact: HIGH
impactDescription: 런타임 타입 안전성 보장
tags: typescript, type-safety, assertion
---

## Type Assertion 금지

`as` type assertion과 non-null assertion `!`을 사용하지 않는다. type guard, conditional rendering, 올바른 타입 설계로 해결한다.

**Incorrect (type assertion 사용):**

```tsx
const name = user as string;
const value = ref.current!;
```

**Correct (type guard / conditional rendering):**

```tsx
// type guard
if (typeof user === 'string') { ... }

// conditional rendering
{value && <Component data={value} />}

// 올바른 타입 설계
const [value, setValue] = useState<TargetType | null>(null);
```
