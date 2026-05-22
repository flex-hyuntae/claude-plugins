---
title: 데이터 레이어 응집
impact: HIGH
impactDescription: 데이터 조작 로직의 응집도 향상
tags: structure, react-query, data-layer, mutation
---

## 데이터 레이어 응집

`invalidateQueries` / `setQueryData` 등 cache 조작은 query / mutation 정의 안에서 처리한다. 뷰는 데이터를 consume 만 한다.

queryKey 자체도 컴포넌트가 직접 만들지 말고 query factory 의 `baseQueryKey` 또는 `options(...).queryKey` 를 참조한다 (→ `flex/react-query-factory.md`).

```tsx
// ❌ 컴포넌트가 raw key 로 직접 invalidate
queryClient.invalidateQueries({ queryKey: ['knowledge-list'] });

// ✅ mutation 의 onSettled / callback 에서 처리
const useUpdateGoal = () =>
  useMutation({
    mutationFn: updateGoalApi,
    onSettled: () =>
      queryClient.invalidateQueries({
        queryKey: knowledgeListQueries.baseQueryKey,
      }),
  });
```
