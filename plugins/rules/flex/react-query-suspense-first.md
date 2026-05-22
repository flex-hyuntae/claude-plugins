---
title: React Query — Suspense 우선
impact: MEDIUM
impactDescription: 컴포넌트 본문 단순화, 로딩/에러 일괄 처리
tags: react-query, suspense, async, flex
---

## React Query — Suspense 우선

기본은 `useSuspenseQuery` / `useSuspenseInfiniteQuery`. 선언적이고 상위 `QueryAsyncBoundary` 에서 pending / rejected 를 일괄 처리.

query 호출은 query factory 의 `options(...)` 를 통한다 (→ `flex/react-query-factory.md`).

```tsx
function KnowledgeList() {
  const { data } = useSuspenseQuery(
    knowledgeListQueries.queries.paginationList(axios).options(params),
  );
  return <Table data={data.list} />;
}

<QueryAsyncBoundary pendingFallback={<Skeleton />} rejectedFallback={<ErrorView />}>
  <KnowledgeList />
</QueryAsyncBoundary>
```

### 비-Suspense (`useQuery`) 가 정당한 경우

- 조건부 조회 (`enabled` 플래그로 fetch 자체를 막아야 함)
- 탭 전환 중 이전 데이터 유지 (`placeholderData: keepPreviousData`)
- UI 가 로딩 상태를 직접 표현 (inline spinner 등)

### 병렬 실행

같은 경계 안에 여러 Suspense 쿼리는 본문에 연속 호출하면 throw 직전까지 각 쿼리가 발사되어 병렬로 실행된다.

```tsx
// ✅ 병렬
function Dashboard() {
  const { data: user } = useSuspenseQuery(userQueries.detail(axios).options());
  const { data: goals } = useSuspenseQuery(goalQueries.list(axios).options());
  return <View user={user} goals={goals} />;
}

// ❌ 직렬 waterfall — 자식이 각자 throw 하면 부모가 자식 resolve 후 다음 자식 mount
<Suspense>
  <UserPanel />
  <GoalPanel />
</Suspense>
```
