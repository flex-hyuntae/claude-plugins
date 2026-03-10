---
name: derived-state-no-effect
title: render 중에 파생 state 계산
impact: MEDIUM
impactDescription: 불필요한 render와 state drift 방지
tags: rerender, derived-state, useEffect, state
---

## render 중에 파생 state 계산

현재 props/state로 계산 가능한 값은 state에 저장하거나 effect에서 업데이트하지 않는다. render 중에 직접 파생하여 불필요한 render와 state drift를 방지한다. prop 변경에 대응하기 위해서만 effect에서 state를 설정하지 말고, 파생 값이나 key reset을 사용한다.

**Incorrect (불필요한 state와 effect):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const [fullName, setFullName] = useState('')

  useEffect(() => {
    setFullName(firstName + ' ' + lastName)
  }, [firstName, lastName])

  return <p>{fullName}</p>
}
```

**Correct (render 중에 파생):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState('First')
  const [lastName, setLastName] = useState('Last')
  const fullName = firstName + ' ' + lastName

  return <p>{fullName}</p>
}
```

참고: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
