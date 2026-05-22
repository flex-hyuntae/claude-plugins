---
title: React Query — Query Factory 패턴
impact: HIGH
impactDescription: params 가 있는 query 의 partial prefix key 를 정의 옆에 묶기
tags: react-query, query-factory, query-key, flex
---

## React Query — Query Factory 패턴

v5 `queryOptions` 는 호출 시 받은 params 까지 포함된 specific queryKey 만 만든다. mutation 이 `setQueriesData` / `invalidateQueries` 로 부분 캐시를 다루려면 params 를 무시한 prefix 가 필요한데 `queryOptions` 가 그걸 제공하지 않는다.

각 query factory 가 `{ baseQueryKey, options }` 를 반환하도록 한다. `baseQueryKey` 가 partial prefix, `options` 는 `queryOptions(...)` (params 없을 때) 또는 `(params) => queryOptions(...)` (params 있을 때).

캐시 키가 3단으로 계층화된다:

| 범위 | 키 | 용도 |
|---|---|---|
| 도메인 전체 | `xxxQueries.baseQueryKey` | 도메인 invalidate |
| query 군 | `xxxQueries.queries.foo(axios).baseQueryKey` | 그 query 의 모든 params 캐시 (`setQueriesData` / `invalidateQueries`) |
| specific 캐시 | `xxxQueries.queries.foo(axios).options(params).queryKey` | `setQueryData` / `getQueryData` |

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
            queryFn: async () => (await searchKnowledges({ searchKnowledgeApiRequest: params })).data,
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

// partial prefix (mutation) — NoInfer 제약상 generic 명시
const queryKey = knowledgeListQueries.queries.paginationList(axios).baseQueryKey;
qc.setQueriesData<SearchKnowledgeApiResponse>({ queryKey }, old => ...);

// specific key — DataTag 추론, generic 불필요
const detailKey = knowledgeDetailQueries.queries.detail(axios).options({ id }).queryKey;
qc.setQueryData(detailKey, old => (old ? { ...old, title } : old));

// 도메인 전체 invalidate
qc.invalidateQueries({ queryKey: knowledgeListQueries.baseQueryKey });
```

### mutation 의 onMutate / onError 는 `effectsOn` 으로 감싸기

`effectsOn<typeof xxxQueries.queries>()({...})` 가 각 query key 에 대해 effect 또는 `null` 을 강제 → 새 query 추가 시 mutation 의 누락이 컴파일 타임에 잡힌다.

```ts
onMutate: variables =>
  effectsOn<typeof knowledgeListQueries.queries>()({
    paginationList: async () => { /* cancel + get + setQueries */ },
    infiniteList: null,
    jiraSpaceList: null,
    googleCalendarList: null,
  }),
onError: (_err, _vars, context) =>
  effectsOn<typeof knowledgeListQueries.queries>()({
    paginationList: () => {
      context?.paginationList?.forEach(([k, d]) => qc.setQueryData(k, d));
      return null;
    },
    infiniteList: null,
    jiraSpaceList: null,
    googleCalendarList: null,
  }),
```

### 안티 패턴

- `partialKeys` 같은 별도 객체에 prefix 만 따로 모아두기 → 정의와 분리되어 새 query 추가 시 키 누락
- `snapshotAndUpdate<T>` 같은 헬퍼로 cache 조작을 감싸기 → v5 의 queryKey DataTag 추론이 헬퍼 generic 으로 가려짐. inline 으로 `cancelQueries` + `getQueriesData` + `setQueriesData` 직접 호출
- specific queryKey 에 `setQueryData<T>` / `getQueryData<T>` generic 명시 → DataTag 추론을 가림
- mutation 의 onError 에서 raw `forEach` 만 호출 → effectsOn 으로 감싸기
