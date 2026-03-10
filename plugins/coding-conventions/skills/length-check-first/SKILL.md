---
name: length-check-first
title: array 비교 시 length 먼저 확인
impact: MEDIUM-HIGH
impactDescription: 길이가 다를 때 비용이 큰 연산 방지
tags: javascript, arrays, performance, optimization, comparison
---

## array 비교 시 length 먼저 확인

비용이 큰 연산(정렬, deep equality, 직렬화)으로 array를 비교할 때 length를 먼저 확인한다. 길이가 다르면 array는 같을 수 없다.

실제 애플리케이션에서 이 최적화는 비교가 hot path(event handler, render loop)에서 실행될 때 특히 유용하다.

**Incorrect (항상 비용이 큰 비교를 실행):**

```typescript
function hasChanges(current: Array<string>, original: Array<string>) {
  // Always sorts and joins, even when lengths differ
  return current.sort().join() !== original.sort().join()
}
```

`current.length`가 5이고 `original.length`가 100이어도 O(n log n) 정렬 두 번이 실행된다. array를 join하고 문자열을 비교하는 overhead도 있다.

**Correct (O(1) length 확인 먼저):**

```typescript
function hasChanges(current: Array<string>, original: Array<string>) {
  // Early return if lengths differ
  if (current.length !== original.length) {
    return true
  }
  // Only sort when lengths match
  const currentSorted = current.toSorted()
  const originalSorted = original.toSorted()
  for (let i = 0; i < currentSorted.length; i++) {
    if (currentSorted[i] !== originalSorted[i]) {
      return true
    }
  }
  return false
}
```

이 접근이 더 효율적인 이유:
- 길이가 다를 때 정렬과 join의 overhead를 피함
- join된 문자열의 메모리 소비를 피함 (큰 array에서 특히 중요)
- 원본 array의 mutation을 피함
- 차이가 발견되면 즉시 반환
