---
title: 일시적인 값에 useRef 사용
impact: MEDIUM
impactDescription: 빈번한 업데이트 시 불필요한 re-render 방지
tags: rerender, useref, state, performance
---

## 일시적인 값에 useRef 사용

값이 자주 변경되고 매 업데이트마다 re-render가 필요 없을 때(mouse tracker, interval, 일시적 flag 등), `useState` 대신 `useRef`에 저장한다. component state는 UI용으로 유지하고, ref는 일시적인 DOM 관련 값에 사용한다. ref 업데이트는 re-render를 발생시키지 않는다.

**Incorrect (매 업데이트마다 render):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: lastX,
        width: 8,
        height: 8,
        background: 'black',
      }}
    />
  )
}
```

**Correct (tracking에 re-render 없음):**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      const node = dotRef.current
      if (node) {
        node.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div
      ref={dotRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: 8,
        height: 8,
        background: 'black',
        transform: 'translateX(0px)',
      }}
    />
  )
}
```
