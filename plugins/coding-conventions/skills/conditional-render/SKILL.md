---
name: conditional-render
description: "&& 연산자 대신 삼항 연산자를 사용하여 falsy 값(0, NaN)이 UI에 렌더링되는 버그를 방지한다. React 컴포넌트에서 조건부 렌더링을 작성할 때, 특히 숫자나 빈 문자열이 조건으로 사용될 수 있는 경우에 적용한다."
title: 명시적 조건부 rendering 사용
impact: LOW
impactDescription: 0이나 NaN이 rendering되는 것을 방지
tags: rendering, conditional, jsx, falsy-values
---

## 명시적 조건부 rendering 사용

조건이 `0`, `NaN`, 또는 다른 falsy 값이 될 수 있을 때 `&&` 대신 명시적 삼항 연산자(`? :`)를 사용한다.

**Incorrect (count가 0일 때 "0"이 rendering됨):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  )
}

// When count = 0, renders: <div>0</div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```

**Correct (count가 0일 때 아무것도 rendering하지 않음):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  )
}

// When count = 0, renders: <div></div>
// When count = 5, renders: <div><span class="badge">5</span></div>
```
