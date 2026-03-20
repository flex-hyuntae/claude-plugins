---
title: 불변성을 위해 sort() 대신 toSorted() 사용
impact: MEDIUM-HIGH
impactDescription: React state의 mutation 버그 방지
tags: javascript, arrays, immutability, react, state, mutation
---

## 불변성을 위해 sort() 대신 toSorted() 사용

`.sort()`는 array를 제자리에서 변경(mutate)하여 React state와 props에서 버그를 일으킬 수 있다. `.toSorted()`를 사용하여 mutation 없이 새 정렬된 array를 생성한다.

**Incorrect (원본 array를 mutate):**

```typescript
function UserList({ users }: { users: Array<User> }) {
  // Mutates the users prop array!
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**Correct (새 array 생성):**

```typescript
function UserList({ users }: { users: Array<User> }) {
  // Creates new sorted array, original unchanged
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users]
  )
  return <div>{sorted.map(renderUser)}</div>
}
```

**React에서 중요한 이유:**

1. Props/state mutation은 React의 불변성 모델을 깨뜨린다 - React는 props와 state를 read-only로 취급하도록 기대한다
2. Stale closure 버그를 유발한다 - closure(callback, effect) 내부에서 array를 mutate하면 예상치 못한 동작이 발생할 수 있다

**Browser 지원 (구형 browser fallback):**

`.toSorted()`는 모든 최신 browser에서 사용 가능하다 (Chrome 110+, Safari 16+, Firefox 115+, Node.js 20+). 구형 환경에서는 spread 연산자를 사용한다:

```typescript
// Fallback for older browsers
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**기타 immutable array method:**

- `.toSorted()` - immutable sort
- `.toReversed()` - immutable reverse
- `.toSpliced()` - immutable splice
- `.with()` - immutable element 교체
