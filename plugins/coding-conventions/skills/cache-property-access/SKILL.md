---
name: cache-property-access
description: 반복문 내에서 동일한 객체 속성을 여러 번 접근하는 대신 지역 변수에 캐싱한다. hot path나 대량 데이터를 순회하는 루프에서 같은 property를 반복 참조하는 코드를 작성하거나 리뷰할 때 적용한다.
title: loop 내 property 접근 캐싱
impact: LOW-MEDIUM
impactDescription: 조회 횟수 감소
tags: javascript, loops, optimization, caching
---

## loop 내 property 접근 캐싱

hot path에서 객체 property 조회를 캐싱한다.

**Incorrect (3번 조회 x N번 반복):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct (총 1번 조회):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```
