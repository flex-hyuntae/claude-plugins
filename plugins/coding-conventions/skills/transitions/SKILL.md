---
name: transitions
description: startTransition을 사용하여 긴급하지 않은 state 업데이트의 우선순위를 낮추고 UI 응답성을 유지한다. 스크롤, 필터링, 검색 등 빈번한 업데이트가 UI를 버벅이게 하는 경우, 또는 무거운 리렌더를 유발하는 state 업데이트를 지연시키고 싶을 때 적용한다.
title: 긴급하지 않은 업데이트에 Transition 사용
impact: MEDIUM
impactDescription: UI 응답성 유지
tags: rerender, transitions, startTransition, performance
---

## 긴급하지 않은 업데이트에 Transition 사용

빈번하고 긴급하지 않은 state 업데이트를 transition으로 표시하여 UI 응답성을 유지한다.

**Incorrect (매 scroll마다 UI blocking):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```

**Correct (non-blocking 업데이트):**

```tsx
import { startTransition } from 'react'

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])
}
```
