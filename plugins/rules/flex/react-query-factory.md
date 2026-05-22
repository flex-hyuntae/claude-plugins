---
title: React Query — Query Factory 패턴
impact: HIGH
impactDescription: queryKey 일관성 + mutation 의 부분 캐시 조작에서 키 누락 방지
tags: react-query, query-factory, query-key, flex
---

## React Query — Query Factory 패턴

각 query factory 는 `{ baseQueryKey, options }` 를 반환한다. `baseQueryKey` 는 그 query 의 partial prefix, `options` 는 `queryOptions(...)` (params 없을 때) 또는 `(params) => queryOptions(...)` (params 있을 때).

mutation 이 `setQueriesData` / `invalidateQueries` 로 부분 캐시를 다룰 때 query 정의 옆의 같은 `baseQueryKey` 를 그대로 참조하므로 key 가 흩어지지 않고 새 query 추가 시 누락이 어렵다.

### 골격

```ts
const knowledgeListQueries = {
  baseQueryKey: ['knowledge-list'] as const,
  queries: {
    paginationList: (axiosInstance: AxiosInstance) => {
      const baseQueryKey = [
        ...knowledgeListQueries.baseQueryKey,
        'pagination-list',
      ] as const;
      const [searchKnowledges] = searchKnowledgesRemote(axiosInstance);
      return {
        baseQueryKey,
        options: (params: SearchKnowledgeApiRequest) =>
          queryOptions({
            queryKey: [...baseQueryKey, params] as const,
            queryFn: async () => {
              const result = await searchKnowledges({ searchKnowledgeApiRequest: params });
              return result.data;
            },
          }),
      };
    },
    category: (axiosInstance: AxiosInstance) => {
      const baseQueryKey = [...knowledgeListQueries.baseQueryKey, 'category'] as const;
      const [getKnowledgeCategories] = getKnowledgeCategoriesRemote(axiosInstance);
      return {
        baseQueryKey,
        options: () =>
          queryOptions({
            queryKey: baseQueryKey,
            queryFn: async () => (await getKnowledgeCategories()).data,
          }),
      };
    },
  },
};
```

### 사용

```ts
// useQuery / useSuspenseQuery
useSuspenseQuery(knowledgeListQueries.queries.paginationList(axios).options(params));
useSuspenseQuery(knowledgeListQueries.queries.category(axios).options());

// mutation 의 부분 캐시 조작 — query 옆의 baseQueryKey 그대로 사용
const queryKey = knowledgeListQueries.queries.paginationList(axios).baseQueryKey;
await qc.cancelQueries({ queryKey });
qc.setQueriesData<SearchKnowledgeApiResponse>({ queryKey }, old => ...);

// 도메인 전체 invalidate
qc.invalidateQueries({ queryKey: knowledgeListQueries.baseQueryKey });
```

### 안티 패턴

- `partialKeys` 같은 별도 객체에 prefix 만 따로 모아두기 → 정의와 사용이 떨어져 새 query 추가 시 키 누락
- `snapshotAndUpdate<T>` 같은 헬퍼로 mutation 의 cache 조작을 감싸기 → query 정의의 queryKey 가 가진 data 타입 inference 가 헬퍼 generic 으로 가려짐. inline 으로 `cancelQueries` + `getQueriesData` + `setQueriesData` 직접 호출
