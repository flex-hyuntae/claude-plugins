---
name: memo-extract
description: 비용이 큰 연산을 별도의 메모이즈된 컴포넌트로 추출하여, 관련 없는 state 변경 시 해당 연산을 건너뛸 수 있게 한다. 컴포넌트 내부에 무거운 계산이나 렌더링이 있고, 해당 계산과 무관한 state 변경으로 인해 불필요하게 재실행되는 경우에 적용한다.
title: Memoized component로 추출
impact: MEDIUM
impactDescription: early return 가능
tags: rerender, memo, useMemo, optimization
---

## Memoized component로 추출

비용이 큰 작업을 memoized component로 추출하여, 연산 전에 early return할 수 있게 한다.

**Incorrect (loading 중에도 avatar를 계산):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])

  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**Correct (loading일 때 연산을 건너뜀):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

**참고:** [React Compiler](https://react.dev/learn/react-compiler)가 활성화되어 있으면 `memo()`, `useMemo()`를 수동으로 사용할 필요 없다. Compiler가 자동으로 re-render를 최적화한다.
