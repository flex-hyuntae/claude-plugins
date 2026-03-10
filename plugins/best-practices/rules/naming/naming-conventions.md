---
title: 네이밍 및 컨벤션
impact: MEDIUM
impactDescription: 코드 가독성 및 일관성 향상
tags: naming, conventions, i18n, documentation
---

## 네이밍 및 컨벤션

일관된 네이밍과 컨벤션을 준수한다.

### 컴포넌트 / 함수 네이밍

**Incorrect:**

```typescript
// 모호한 이름
function process(data: Array<User>) { ... }
function handleClick() { ... } // 여러 버튼이 있는 컴포넌트에서

const MyComp = () => { ... } // 역할이 불명확
```

**Correct:**

```typescript
// 의도를 명확히 드러내는 이름
function filterActiveUsers(users: Array<User>) { ... }
function handleDeleteButtonClick() { ... }

const UserProfileCard = () => { ... }
```

### 이벤트 핸들러 네이밍

```typescript
// Props: on + 동사 (이벤트 전달)
interface Props {
  onSubmit: () => void;
  onChange: (value: string) => void;
}

// 내부 핸들러: handle + 대상 + 동사
function handleFormSubmit() { ... }
function handleNameChange(value: string) { ... }
```

### 주석 규칙

```typescript
// ❌ what을 설명하는 불필요한 주석
// 유저를 필터링한다
const activeUsers = users.filter((u) => u.isActive);

// ✅ why를 설명하는 필요한 주석
// 비활성 유저는 결재선에 포함되지 않아야 한다 (정책 CORE-1234)
const activeUsers = users.filter((u) => u.isActive);
```
