---
name: index-maps
description: 반복적인 key 기반 조회를 위해 배열을 Map으로 변환하여 O(n) find()를 O(1) get()으로 개선한다. 중첩 루프나 반복문 안에서 .find()로 다른 배열을 탐색하는 패턴, 또는 대량 데이터에서 ID 기반 매칭이 필요한 경우에 적용한다.
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
