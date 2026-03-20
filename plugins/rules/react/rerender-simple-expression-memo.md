---
title: primitive 결과의 단순 표현식을 useMemo로 감싸지 않기
impact: LOW-MEDIUM
impactDescription: 매 render마다 낭비되는 연산
tags: rerender, useMemo, optimization
---

## primitive 결과의 단순 표현식을 useMemo로 감싸지 않기

표현식이 단순하고(논리/산술 연산자 몇 개) 결과 타입이 primitive(boolean, number, string)이면 `useMemo`로 감싸지 않는다.
`useMemo` 호출과 hook dependency 비교가 표현식 자체보다 더 많은 리소스를 소비할 수 있다.

**Incorrect:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])

  if (isLoading) return <Skeleton />
  // return some markup
}
```

**Correct:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading

  if (isLoading) return <Skeleton />
  // return some markup
}
```
