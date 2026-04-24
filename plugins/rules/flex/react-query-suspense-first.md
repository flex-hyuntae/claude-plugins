---
title: React Query — Suspense 우선
impact: MEDIUM
impactDescription: 컴포넌트 본문 단순화, 로딩/에러 일괄 처리
tags: react-query, suspense, async, flex
---

## React Query — Suspense 우선

기본은 `useSuspenseQuery` / `useSuspenseInfiniteQuery`를 선택한다. 선언적이고, 상위 `QueryAsyncBoundary`에서 pending/rejected를 일괄 처리해 컴포넌트 본문이 깔끔해진다.

**Correct (Suspense 기반, 본문에 로딩/에러 분기 없음):**

```tsx
function GoalList() {
  const { data } = useSuspenseQuery(goalListQueryOptions());
  return <ul>{data.map(goal => <li key={goal.id}>{goal.name}</li>)}</ul>;
}

// 상위에서 일괄 처리
<QueryAsyncBoundary pendingFallback={<Skeleton />} rejectedFallback={<ErrorView />}>
  <GoalList />
</QueryAsyncBoundary>
```

**비-Suspense(`useQuery`)는 정당한 이유가 있을 때만 선택:**

- 조건부 조회 (`enabled` 플래그로 fetch 자체를 막아야 할 때)
- 탭 전환 중 이전 데이터 유지 (`placeholderData`)
- UI가 로딩 상태를 직접 표현해야 하는 케이스 (inline spinner, skeleton이 아닌 progress 표기 등)

**병렬 실행:**

한 경계 안에 여러 Suspense 쿼리를 배치할 땐 병렬로 실행되도록 선언한다.

```tsx
// 같은 컴포넌트 내 연속 호출 — throw 직전까지 각 쿼리가 실행되므로 병렬
function Dashboard() {
  const { data: user } = useSuspenseQuery(userQueryOptions());
  const { data: goals } = useSuspenseQuery(goalsQueryOptions());
  const { data: reviews } = useSuspenseQuery(reviewsQueryOptions());
  return <View user={user} goals={goals} reviews={reviews} />;
}

// 또는 useSuspenseQueries로 명시적 병렬
const [userQ, goalsQ] = useSuspenseQueries({
  queries: [userQueryOptions(), goalsQueryOptions()],
});
```

**Incorrect (같은 경계 내에서 쿼리가 직렬 실행되는 구조):**

```tsx
// 하위 컴포넌트로 나눠서 각각이 별도 경계에서 throw하면 직렬 waterfall이 된다
<Suspense>
  <UserPanel />      {/* throw → 여기서 멈춤 */}
  <GoalPanel />      {/* UserPanel resolve 후에야 실행 */}
</Suspense>
```
