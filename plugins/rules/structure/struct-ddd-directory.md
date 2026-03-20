---
title: DDD 기반 디렉토리 구조
impact: MEDIUM
impactDescription: 도메인별 응집도 향상
tags: structure, ddd, directory, domain
---

## DDD 기반 디렉토리 구조

기능(component)별이 아닌 도메인/동작별로 그룹핑한다.

**Incorrect (기능별 flat 구조):**

```
components/GoalList/
components/GoalForm/
components/GoalDetail/
hooks/useGoalQuery.ts
queries/goal/
```

**Correct (도메인별 구조):**

```
<domain | category | ...>/
├── components/          # 도메인 관련 컴포넌트들
├── queries/             # React Query (useQueryOptionsFactory 등)
├── hooks/               # 도메인 전용 훅
├── utils/               # 유틸 함수
└── models/              # 타입 정의
```

- 각 도메인은 자체적으로 components, queries, hooks 등을 보유
- queries 내에서 `useQueryOptionsFactory` 패턴으로 queryOptions 추상화
- 계층적 query key 관리 (`['domain', 'action', params]`)
