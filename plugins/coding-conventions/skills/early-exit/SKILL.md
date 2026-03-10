---
name: early-exit
description: 결과가 확정된 시점에서 즉시 return하여 불필요한 후속 처리를 건너뛴다. 유효성 검사, 에러 처리, 조건 분기가 있는 함수에서 조건 충족 후에도 나머지 로직이 계속 실행되는 코드를 작성하거나 리뷰할 때 적용한다.
title: 함수에서 early return
impact: LOW-MEDIUM
impactDescription: 불필요한 연산 방지
tags: javascript, functions, optimization, early-return
---

## 함수에서 early return

결과가 결정되면 즉시 반환하여 불필요한 처리를 건너뛴다.

**Incorrect (답을 찾은 후에도 모든 항목을 처리):**

```typescript
function validateUsers(users: Array<User>) {
  let hasError = false
  let errorMessage = ''

  for (const user of users) {
    if (!user.email) {
      hasError = true
      errorMessage = 'Email required'
    }
    if (!user.name) {
      hasError = true
      errorMessage = 'Name required'
    }
    // Continues checking all users even after error found
  }

  return hasError ? { valid: false, error: errorMessage } : { valid: true }
}
```

**Correct (첫 번째 에러에서 즉시 반환):**

```typescript
function validateUsers(users: Array<User>) {
  for (const user of users) {
    if (!user.email) {
      return { valid: false, error: 'Email required' }
    }
    if (!user.name) {
      return { valid: false, error: 'Name required' }
    }
  }

  return { valid: true }
}
```
