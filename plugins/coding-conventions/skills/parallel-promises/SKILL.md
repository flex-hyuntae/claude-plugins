---
name: parallel-promises
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
