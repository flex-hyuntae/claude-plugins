---
title: any 타입 사용 금지
impact: HIGH
impactDescription: 런타임 타입 안전성 보장
tags: typescript, type-safety, any
---

## any 타입 사용 금지

`any` 타입을 사용하지 않는다. 적절한 타입, `unknown`, 또는 제네릭으로 대체한다.

**Incorrect (any 사용):**

```typescript
const data: any = fetchData();
function process(value: any) { return value.name; }
const config: Record<string, any> = {};
```

**Correct (구체적 타입 사용):**

```typescript
// 적절한 타입 정의
interface FetchResult {
  data: string;
  status: number;
}
const data: FetchResult = fetchData();

// unknown + type guard
const result: unknown = fetchData();
if (isValidResult(result)) {
  return result.name;
}

// 구체적 union 타입
const config: Record<string, string | number | boolean> = {};
```
