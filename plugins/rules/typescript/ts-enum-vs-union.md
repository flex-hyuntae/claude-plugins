---
title: enum 대신 union type 사용
impact: HIGH
impactDescription: 번들 사이즈 감소 및 타입 안전성 향상
tags: typescript, enum, union, type-safety
---

## enum 대신 union type 사용

TypeScript enum 대신 union type을 사용한다. enum은 런타임 코드를 생성하여 번들 사이즈를 증가시키고, tree-shaking이 어렵다.

**Incorrect (enum 사용):**

```typescript
enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Pending = "PENDING",
}

function getLabel(status: Status): string {
  switch (status) {
    case Status.Active:
      return "활성";
    case Status.Inactive:
      return "비활성";
    case Status.Pending:
      return "대기";
  }
}
```

**Correct (union type 사용):**

```typescript
type Status = "ACTIVE" | "INACTIVE" | "PENDING";

const STATUS_LABEL: Record<Status, string> = {
  ACTIVE: "활성",
  INACTIVE: "비활성",
  PENDING: "대기",
};

function getLabel(status: Status): string {
  return STATUS_LABEL[status];
}
```

**`as const` 객체가 필요한 경우:**

```typescript
const STATUS = {
  Active: "ACTIVE",
  Inactive: "INACTIVE",
  Pending: "PENDING",
} as const;

type Status = (typeof STATUS)[keyof typeof STATUS];
```
