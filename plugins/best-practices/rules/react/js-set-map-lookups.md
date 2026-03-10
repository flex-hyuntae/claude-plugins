---
title: O(1) 조회를 위한 Set/Map 사용
impact: LOW-MEDIUM
impactDescription: O(n) → O(1)
tags: javascript, set, map, data-structures, performance
---

## O(1) 조회를 위한 Set/Map 사용

반복적인 포함 여부 확인을 위해 array를 Set/Map으로 변환한다.

**Incorrect (확인당 O(n)):**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**Correct (확인당 O(1)):**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```
