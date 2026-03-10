---
title: 함수형 setState 업데이트 사용
impact: MEDIUM
impactDescription: stale closure 방지 및 불필요한 callback 재생성 제거
tags: react, hooks, useState, useCallback, callbacks, closures
---

## 함수형 setState 업데이트 사용

현재 state 값에 기반하여 state를 업데이트할 때는, state 변수를 직접 참조하지 말고 setState의 함수형 업데이트를 사용한다. stale closure를 방지하고, 불필요한 dependency를 제거하며, 안정적인 callback reference를 만든다.

**Incorrect (state를 dependency로 필요로 함):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)

  // Callback must depend on items, recreated on every items change
  const addItems = useCallback((newItems: Array<Item>) => {
    setItems([...items, ...newItems])
  }, [items])  // items dependency causes recreations

  // Risk of stale closure if dependency is forgotten
  const removeItem = useCallback((id: string) => {
    setItems(items.filter(item => item.id !== id))
  }, [])  // Missing items dependency - will use stale items!

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

첫 번째 callback은 `items`가 변경될 때마다 재생성되어 자식 component의 불필요한 re-render를 유발한다. 두 번째 callback은 stale closure 버그가 있어 항상 초기 `items` 값을 참조한다.

**Correct (안정적인 callback, stale closure 없음):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)

  // Stable callback, never recreated
  const addItems = useCallback((newItems: Array<Item>) => {
    setItems(curr => [...curr, ...newItems])
  }, [])  // No dependencies needed

  // Always uses latest state, no stale closure risk
  const removeItem = useCallback((id: string) => {
    setItems(curr => curr.filter(item => item.id !== id))
  }, [])  // Safe and stable

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />
}
```

**장점:**

1. **안정적인 callback reference** - state가 변경되어도 callback을 재생성할 필요 없음
2. **stale closure 없음** - 항상 최신 state 값으로 동작
3. **dependency 감소** - dependency array가 단순해지고 memory leak 감소
4. **버그 방지** - React closure 버그의 가장 흔한 원인 제거

**함수형 업데이트를 사용해야 할 때:**

- 현재 state 값에 의존하는 모든 setState
- state가 필요한 useCallback/useMemo 내부
- state를 참조하는 event handler
- state를 업데이트하는 async 작업

**직접 업데이트가 괜찮은 경우:**

- 정적 값으로 state 설정: `setCount(0)`
- props/arguments로만 state 설정: `setName(newName)`
- 이전 값에 의존하지 않는 state

**참고:** [React Compiler](https://react.dev/learn/react-compiler)가 활성화되어 있으면 일부 케이스를 자동 최적화할 수 있지만, 정확성과 stale closure 버그 방지를 위해 함수형 업데이트가 여전히 권장된다.
