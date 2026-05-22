---
title: React Query — Query Factory 패턴
impact: HIGH
impactDescription: params 가 있는 query 의 partial prefix key 를 정의 옆에 묶기
tags: react-query, query-factory, query-key, flex
---

## React Query — Query Factory 패턴

v5 `queryOptions` 는 호출 시 받은 params 까지 포함된 specific queryKey 만 만든다.

```ts
queries: {
  foo: (params) => queryOptions({ queryKey: [...baseQueryKey, 'foo', params], ... }),
  bar: ()       => queryOptions({ queryKey: [...baseQueryKey, 'bar'],         ... }),
}
```

- `bar` 는 params 가 없어 `queries.bar().queryKey` 가 partial prefix 로도 그대로 쓰임
- `foo` 는 mutation 시점에 어떤 params 가 캐시에 있는지 알 수 없어 params 를 무시한 prefix (`[...baseQueryKey, 'foo']`) 가 필요한데, `queryOptions` 가 그걸 제공하지 않는다

각 query factory 가 `{ baseQueryKey, options }` 를 반환하도록 한다. `baseQueryKey` 가 params 를 무시한 partial prefix, `options` 는 `queryOptions(...)` (params 없을 때) 또는 `(params) => queryOptions(...)` (params 있을 때).

캐시 범위가 3단으로 계층화된다:

| 범위 | 키 | 용도 |
|---|---|---|
| 도메인 전체 | `knowledgeListQueries.baseQueryKey` | 도메인 invalidate |
| 특정 query 군 | `knowledgeListQueries.queries.paginationList(axios).baseQueryKey` | 그 query 의 모든 params 캐시에 대한 `setQueriesData` / `invalidateQueries` |
| 특정 params 캐시 | `knowledgeListQueries.queries.paginationList(axios).options(params).queryKey` | `setQueryData` / `getQueryData` (specific) |

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

// mutation 의 부분 캐시 조작 — params 무시한 prefix 사용
const queryKey = knowledgeListQueries.queries.paginationList(axios).baseQueryKey;
await qc.cancelQueries({ queryKey });
qc.setQueriesData<SearchKnowledgeApiResponse>({ queryKey }, old => ...);

// 도메인 전체 invalidate
qc.invalidateQueries({ queryKey: knowledgeListQueries.baseQueryKey });
```

### 안티 패턴

- `partialKeys` 같은 별도 객체에 prefix 만 따로 모아두기 → 정의와 분리되어 새 query 추가 시 키 누락
- `snapshotAndUpdate<T>` 같은 헬퍼로 mutation 의 cache 조작을 감싸기 → query 정의의 queryKey 가 가진 data 타입 inference 가 헬퍼 generic 으로 가려짐. inline 으로 `cancelQueries` + `getQueriesData` + `setQueriesData` 직접 호출
