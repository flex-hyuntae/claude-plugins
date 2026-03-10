---
title: RegExp 생성을 끌어올리기
impact: LOW-MEDIUM
impactDescription: 재생성 방지
tags: javascript, regexp, optimization, memoization
---

## RegExp 생성을 끌어올리기

render 내부에서 RegExp를 생성하지 않는다. module scope로 끌어올리거나 `useMemo()`로 memoize한다.

**Incorrect (매 render마다 새 RegExp):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**Correct (memoize 또는 끌어올리기):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**주의 (global regex는 mutable state를 가짐):**

Global regex(`/g`)는 mutable `lastIndex` state를 가진다:

```typescript
const regex = /foo/g
regex.test('foo')  // true, lastIndex = 3
regex.test('foo')  // false, lastIndex = 0
```
