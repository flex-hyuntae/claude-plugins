---
name: derived-state
title: 파생 state 구독
impact: MEDIUM
impactDescription: re-render 빈도 감소
tags: rerender, derived-state, media-query, optimization
---

## 파생 state 구독

연속적인 값 대신 파생된 boolean state를 구독하여 re-render 빈도를 줄인다.

**Incorrect (pixel이 바뀔 때마다 re-render):**

```tsx
function Sidebar() {
  const width = useWindowWidth()  // updates continuously
  const isMobile = width < 768
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```

**Correct (boolean이 바뀔 때만 re-render):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery('(max-width: 767px)')
  return <nav className={isMobile ? 'mobile' : 'desktop'} />
}
```
