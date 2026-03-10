---
name: index-maps
title: 반복 조회를 위한 Index Map 구축
impact: LOW-MEDIUM
impactDescription: 100만 ops → 2천 ops
tags: javascript, map, indexing, optimization, performance
---

## 반복 조회를 위한 Index Map 구축

같은 key로 `.find()`를 여러 번 호출하면 Map을 사용해야 한다.

**Incorrect (조회당 O(n)):**

```typescript
function processOrders(orders: Array<Order>, users: Array<User>) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**Correct (조회당 O(1)):**

```typescript
function processOrders(orders: Array<Order>, users: Array<User>) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

Map을 한 번 구축(O(n))하면 모든 조회가 O(1)이 된다.
1000 orders x 1000 users 기준: 100만 ops → 2천 ops.
