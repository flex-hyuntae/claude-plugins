---
name: transitions
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
