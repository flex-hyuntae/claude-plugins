---
name: lazy-state-init
title: 지연 state 초기화 사용
impact: MEDIUM
impactDescription: 매 render마다 낭비되는 연산
tags: react, hooks, useState, performance, initialization
---

## 지연 state 초기화 사용

비용이 큰 초기값에는 `useState`에 함수를 전달한다. 함수 형태를 사용하지 않으면, 값이 한 번만 사용됨에도 초기화 로직이 매 render마다 실행된다.

**Incorrect (매 render마다 실행):**

```tsx
function FilteredList({ items }: { items: Array<Item> }) {
  // buildSearchIndex() runs on EVERY render, even after initialization
  const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
  const [query, setQuery] = useState('')

  // When query changes, buildSearchIndex runs again unnecessarily
  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse runs on every render
  const [settings, setSettings] = useState(
    JSON.parse(localStorage.getItem('settings') || '{}')
  )

  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

**Correct (한 번만 실행):**

```tsx
function FilteredList({ items }: { items: Array<Item> }) {
  // buildSearchIndex() runs ONLY on initial render
  const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
  const [query, setQuery] = useState('')

  return <SearchResults index={searchIndex} query={query} />
}

function UserProfile() {
  // JSON.parse runs only on initial render
  const [settings, setSettings] = useState(() => {
    const stored = localStorage.getItem('settings')
    return stored ? JSON.parse(stored) : {}
  })

  return <SettingsForm settings={settings} onChange={setSettings} />
}
```

localStorage/sessionStorage에서 초기값을 읽거나, data structure(index, map)를 구축하거나, DOM에서 읽거나, 무거운 변환을 수행할 때 지연 초기화를 사용한다.

단순 primitive(`useState(0)`), 직접 참조(`useState(props.value)`), 저렴한 literal(`useState({})`)에는 함수 형태가 불필요하다.
