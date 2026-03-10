---
name: set-map-lookups
description: 반복적인 멤버십 확인을 위해 배열을 Set이나 Map으로 변환하여 O(n) includes()를 O(1) has()로 개선한다. .includes()나 .indexOf()로 배열 내 존재 여부를 반복 확인하는 코드를 발견했을 때 적용한다.
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
