---
title: 상호작용 로직을 event handler에 배치
impact: MEDIUM
impactDescription: effect 재실행과 side effect 중복 방지
tags: rerender, useEffect, events, side-effects, dependencies
---

## 상호작용 로직을 event handler에 배치

side effect가 특정 사용자 action(submit, click, drag)에 의해 발생하면, 해당 event handler에서 실행한다. action을 state + effect로 모델링하면 관련 없는 변경에도 effect가 재실행되고 action이 중복될 수 있다.

**Incorrect (event를 state + effect로 모델링):**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post('/api/register')
      showToast('Registered', theme)
    }
  }, [submitted, theme])

  return <button onClick={() => setSubmitted(true)}>Submit</button>
}
```

**Correct (handler에서 직접 실행):**

```tsx
function Form() {
  const theme = useContext(ThemeContext)

  function handleSubmit() {
    post('/api/register')
    showToast('Registered', theme)
  }

  return <button onClick={handleSubmit}>Submit</button>
}
```

참고: [Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)
