---
name: narrow-dependencies
title: Effect dependency를 좁게 지정
impact: LOW
impactDescription: effect 재실행 최소화
tags: rerender, useEffect, dependencies, optimization
---

## Effect dependency를 좁게 지정

객체 대신 primitive dependency를 지정하여 effect 재실행을 최소화한다.

**Incorrect (user의 어떤 필드가 변경되어도 재실행):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**Correct (id가 변경될 때만 재실행):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**파생 state는 effect 외부에서 계산:**

```tsx
// Incorrect: runs on width=767, 766, 765...
useEffect(() => {
  if (width < 768) {
    enableMobileMode()
  }
}, [width])

// Correct: runs only on boolean transition
const isMobile = width < 768
useEffect(() => {
  if (isMobile) {
    enableMobileMode()
  }
}, [isMobile])
```
