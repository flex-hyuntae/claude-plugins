---
title: React Query — Query Factory 패턴
impact: HIGH
impactDescription: queryKey 일관성 + v5 type inference 활용 + mutation 의 부분 캐시 조작 단순화
tags: react-query, query-factory, query-key, flex
---

## React Query — Query Factory 패턴

도메인 단위로 query factory 객체를 만든다. 각 factory 는 `{ baseQueryKey, options }` 를 반환하고, options 는 params 가 있는 경우 함수, 없는 경우 객체이다.

`baseQueryKey` 가 그 query 군의 partial prefix 역할을 한다. mutation 의 `setQueriesData` / `invalidateQueries` 가 query 정의 옆의 같은 `baseQueryKey` 를 그대로 참조하므로 key 가 흩어지지 않는다.

### 기본 골격

```ts
import { queryOptions, infiniteQueryOptions } from '@tanstack/react-query-v5';

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
    infiniteList: (axiosInstance: AxiosInstance) => {
      const baseQueryKey = [
        ...knowledgeListQueries.baseQueryKey,
        'infinite-list',
      ] as const;
      const [searchKnowledges] = searchKnowledgesRemote(axiosInstance);
      return {
        baseQueryKey,
        options: (params: Omit<SearchKnowledgeApiRequest, 'page'>) =>
          infiniteQueryOptions({
            queryKey: [...baseQueryKey, params] as const,
            queryFn: async ({ pageParam }) => {
              const result = await searchKnowledges({
                searchKnowledgeApiRequest: { ...params, page: pageParam },
              });
              return result.data;
            },
            initialPageParam: 0,
            getNextPageParam: lastPage =>
              lastPage.meta && lastPage.meta.page + 1 < lastPage.meta.totalPages
                ? lastPage.meta.page + 1
                : undefined,
          }),
      };
    },
    // params 가 없으면 options 는 객체로 반환해도 되고, 일관성을 위해 () => queryOptions(...) 로 만들어도 된다.
    category: (axiosInstance: AxiosInstance) => {
      const baseQueryKey = [
        ...knowledgeListQueries.baseQueryKey,
        'category',
      ] as const;
      const [getKnowledgeCategories] = getKnowledgeCategoriesRemote(axiosInstance);
      return {
        baseQueryKey,
        options: () =>
          queryOptions({
            queryKey: baseQueryKey,
            queryFn: async () => {
              const { data } = await getKnowledgeCategories();
              return data;
            },
          }),
      };
    },
  },
};

export { knowledgeListQueries };
```

### useQuery / useSuspenseQuery 호출

```tsx
// params 가 있는 query
const { data } = useSuspenseQuery({
  ...knowledgeListQueries.queries.paginationList(instances.json).options({
    page: 0,
    size: 50,
    keyword,
  }),
  select: data => data.list,
});

// params 가 없는 query
const { data } = useSuspenseQuery({
  ...knowledgeListQueries.queries.category(instances.json).options(),
});
```

### mutation 의 부분 캐시 조작

각 query 의 `baseQueryKey` 가 그대로 `setQueriesData` / `invalidateQueries` 의 partial prefix 가 된다.

```ts
onMutate: variables =>
  effectsOn<typeof knowledgeListQueries.queries>()({
    paginationList: async () => {
      const queryKey = knowledgeListQueries.queries
        .paginationList(axiosInstance)
        .baseQueryKey;
      await qc.cancelQueries({ queryKey });
      const previous = qc.getQueriesData<SearchKnowledgeApiResponse>({ queryKey });
      qc.setQueriesData<SearchKnowledgeApiResponse>({ queryKey }, old =>
        old
          ? { ...old, list: old.list.filter(item => !ids.includes(item.id)) }
          : old
      );
      return previous;
    },
    infiniteList: null,
  }),
onError: (_err, _vars, context) => {
  context?.paginationList?.forEach(([queryKey, data]) => {
    qc.setQueryData(queryKey, data);
  });
},
```

전체 도메인 invalidate 가 필요하면 최상위 `baseQueryKey` 를 그대로 쓴다.

```ts
qc.invalidateQueries({ queryKey: knowledgeListQueries.baseQueryKey });
```

### 안티 패턴

**Incorrect — partial key 를 별도 객체로 분리:** query 정의와 key 정의가 두 곳으로 갈라져 새 query 추가 시 누락된다.

```ts
const knowledgeListQueries = {
  baseQueryKey: ['knowledge-list'] as const,
  partialKeys: {
    paginationList: ['knowledge-list', 'pagination-list'] as const, // ❌
  },
  queries: { paginationList: ... },
};
```

**Incorrect — params 와 함께 inline queryKey 만 노출 (`{ baseQueryKey } 없음`)`:** mutation 이 부분 캐시를 조작하려면 partial key 를 매번 inline 으로 다시 작성해야 한다.

```ts
paginationList: (axios, params) =>
  queryOptions({
    queryKey: ['knowledge-list', 'pagination-list', params] as const, // ❌
    queryFn: ...,
  }),
```

**Incorrect — 헬퍼로 generic 명시:** v5 의 queryOptions 가 inference 해주는 data 타입을 잃는다.

```ts
async function snapshotAndUpdate<T>(qc, queryKey, update) { ... }  // ❌
```

mutation 안에서 `qc.cancelQueries` / `qc.getQueriesData` / `qc.setQueriesData` 를 inline 으로 직접 호출한다.
