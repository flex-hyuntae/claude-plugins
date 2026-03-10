---
name: memo-default-value
description: React.memo로 감싼 컴포넌트의 non-primitive 기본값(빈 배열, 빈 객체, 콜백 등)을 모듈 레벨 상수로 추출하여 메모이제이션이 깨지는 것을 방지한다. memo된 컴포넌트에 기본값으로 `[]`, `{}`, `() => {}` 등을 인라인으로 전달하는 코드를 발견했을 때 적용한다.
title: Memoized component의 non-primitive default 값을 상수로 추출
impact: MEDIUM
impactDescription: 상수를 사용하여 memoization 복원
tags: rerender, memo, optimization
---

## Memoized component의 non-primitive default 값을 상수로 추출

Memoized component가 array, function, object 같은 non-primitive optional parameter의 default 값을 가질 때, 해당 parameter 없이 component를 호출하면 memoization이 깨진다. 매 rerender마다 새 인스턴스가 생성되어 `memo()`의 strict equality 비교를 통과하지 못하기 때문이다.

이 문제를 해결하려면 default 값을 상수로 추출한다.

**Incorrect (매 rerender마다 `onClick`이 다른 값):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```

**Correct (안정적인 default 값):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: { onClick?: () => void }) {
  // ...
})

// Used without optional onClick
<UserAvatar />
```
