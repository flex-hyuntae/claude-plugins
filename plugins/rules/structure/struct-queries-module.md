---
title: queries 모듈 — option 만 내보낸다
impact: HIGH
impactDescription: 호출 방식 선택권을 호출자에게 남기고 캐시 조작을 한곳에 모음
tags: structure, react-query, queries, query-options, mutation, data-layer
---

## queries 모듈 — option 만 내보낸다

`queries/` 는 `queryOptions` · mutation option 을 만드는 팩토리다. `useQuery` · `useMutation` 을 부르는 훅을 여기서 만들지 않는다.

option 만 내보내면 같은 쿼리를 `useQuery` 로도, `useSuspenseQuery` 로도, `prefetchQuery` 로도 쓸 수 있다. 훅으로 감싸는 순간 그 선택이 팩토리에 박힌다.

### 이름

동사로 시작하고 `Queries` 또는 `Mutations` 로 끝난다.

- `queries/searchUserQueries.ts`
- `queries/postUserMutations.ts`

### 골격

`queryOptions` 가 만드는 queryKey 는 params 까지 포함된 특정 키다. 캐시를 부분 무효화하려면 params 를 뺀 prefix 가 따로 필요하니 `baseQueryKey` 를 같이 내보낸다.

```ts
// queries/searchUserQueries.ts
export const searchUserQueries = {
  baseQueryKey: ['user'] as const,
  queries: {
    list: (axiosInstance: AxiosInstance) => {
      const baseQueryKey = [...searchUserQueries.baseQueryKey, 'list'] as const;
      return {
        baseQueryKey,
        options: (params: SearchUserRequest) =>
          queryOptions({
            queryKey: [...baseQueryKey, params] as const,
            queryFn: () => searchUsers(axiosInstance, params),
          }),
      };
    },
  },
};
```

키는 세 범위로 쓴다.

| 범위 | 키 |
|---|---|
| 도메인 전체 | `searchUserQueries.baseQueryKey` |
| 한 query 의 모든 params | `searchUserQueries.queries.list(axios).baseQueryKey` |
| 특정 캐시 | `searchUserQueries.queries.list(axios).options(params).queryKey` |

### 호출 방식은 쓰는 쪽이 고른다

```tsx
// ✅ 컴포넌트가 직접 고른다
const { data } = useSuspenseQuery(searchUserQueries.queries.list(axios).options(params));

// ❌ queries 안에서 훅을 만들어 강제
export const useUserList = (params) => useQuery(...);
```

### 데이터의 흐름은 이 모듈 안에서만

`invalidateQueries` · `setQueryData` · optimistic update · rollback 은 전부 query / mutation 정의 안에서 처리한다. 뷰는 데이터를 consume 만 한다. queryKey 도 컴포넌트가 직접 만들지 않고 위 세 범위를 참조한다.

팩토리는 훅이 아니라서 `useQueryClient` 를 부를 수 없다. `queryClient` 를 `axiosInstance` 와 같이 인자로 받는다. 모듈 스코프 싱글턴을 import 하면 테스트마다 캐시가 새로 안 만들어진다.

```tsx
// ❌ 컴포넌트가 raw key 로 직접 invalidate
queryClient.invalidateQueries({ queryKey: ['user'] });

// ✅ mutation 정의 안에서
export const postUserMutations = {
  update: (axiosInstance: AxiosInstance, queryClient: QueryClient) => ({
    options: () => ({
      mutationFn: (body: UpdateUserRequest) => updateUser(axiosInstance, body),
      onSettled: () =>
        queryClient.invalidateQueries({ queryKey: searchUserQueries.baseQueryKey }),
    }),
  }),
};

// 호출부
const mutation = useMutation(postUserMutations.update(axios, useQueryClient()).options());
```
