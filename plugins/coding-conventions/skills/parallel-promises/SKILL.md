---
name: parallel-promises
description: Promise.all()을 사용하여 독립적인 async 작업을 순차가 아닌 병렬로 실행한다. 결과가 서로 의존하지 않는 여러 개의 순차 await, API 호출 waterfall 패턴, 또는 async 코드 속도 개선이 필요한 경우에 적용한다. 가장 효과가 큰 성능 최적화 중 하나(2-10배 개선).
title: 독립적인 작업에 Promise.all() 사용
impact: CRITICAL
impactDescription: 2-10배 개선
tags: async, parallelization, promises, waterfalls
---

## 독립적인 작업에 Promise.all() 사용

async 작업 간 의존성이 없으면 `Promise.all()`로 동시에 실행한다.

**Incorrect (순차 실행, 3번 round trip):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct (병렬 실행, 1번 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```
