---
title: 데이터 레이어 응집
impact: HIGH
impactDescription: 데이터 조작 로직의 응집도 향상
tags: structure, react-query, data-layer, mutation
---

## 데이터 레이어 응집

`invalidateQueries`, `setQueryData` 등 query 데이터 조작은 query/mutation 훅 내부에서 처리한다. 뷰(컴포넌트)는 데이터를 consume만 한다.

**Incorrect (컴포넌트에서 직접 조작):**

```tsx
// component
const queryClient = useQueryClient();
queryClient.invalidateQueries(['goals']);
```

**Correct (mutation 훅 내부에서 처리):**

```tsx
// mutation hook
const useUpdateGoal = () =>
  useMutation({
    mutationFn: updateGoalApi,
    onSettled: () => {
      queryClient.invalidateQueries(['goals']);
    },
  });

// component - UI 피드백만 전달
const { mutate } = useUpdateGoal();
mutate(data, { onSuccess: () => toast.success('저장 완료') });
```
