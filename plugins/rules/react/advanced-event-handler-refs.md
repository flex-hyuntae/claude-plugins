---
title: Event handler를 ref에 저장
impact: LOW
impactDescription: 안정적인 subscription
tags: advanced, hooks, refs, event-handlers, optimization
---

## Event handler를 ref에 저장

callback 변경 시 재구독하면 안 되는 effect에서 사용하는 callback을 ref에 저장한다.

**Incorrect (매 render마다 재구독):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**Correct (안정적인 subscription):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**대안: 최신 React의 `useEffectEvent` 사용:**

```tsx
import { useEffectEvent } from 'react'

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)

  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

`useEffectEvent`는 동일한 패턴을 더 깔끔한 API로 제공한다: 항상 최신 버전의 handler를 호출하는 안정적인 function reference를 생성한다.
