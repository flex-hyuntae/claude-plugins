# Coding Conventions

코드 생성 시 참고할 코딩 컨벤션 및 아키텍처 패턴.

## 컴포넌트 폴더 구조

기본 구조 (항상):

```
ComponentName/
├── index.tsx          # 메인 컴포넌트 (export)
└── style.css.ts       # 스타일 정의
```

필요에 따라 확장:

```
ComponentName/
├── index.tsx          # 메인 컴포넌트 (export)
├── style.css.ts       # 스타일 정의
├── components/        # 하위 컴포넌트
├── hooks/             # 컴포넌트 전용 훅
├── utils/             # 유틸 함수
├── models/            # 타입 정의
└── queries/           # React Query 관련
```

- 기본은 `index.tsx` + `style.css.ts` 2파일로 시작
- 컴포넌트가 복잡해지면 맥락에 맞게 하위 폴더를 추가
- 외부에서 재사용되는 것은 상위 레벨로 분리

## DDD 기반 디렉토리 구조

기능(component)별이 아닌 도메인/동작별로 그룹핑한다.

```
# X - 기능별 flat 구조
components/GoalList/
components/GoalForm/
components/GoalDetail/
hooks/useGoalQuery.ts
queries/goal/

# O - 도메인별 구조
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

## 데이터 레이어 응집

- `invalidateQueries`, `setQueryData` 등 query 데이터 조작은 query/mutation 훅 내부에서 처리한다
- 뷰(컴포넌트)는 데이터를 consume만 한다 (onSuccess 같은 UI 피드백만 전달)
  - ❌ 컴포넌트에서 `queryClient.invalidateQueries(...)` 직접 호출
  - ✅ mutation 훅 내부 `onSettled`에서 `invalidateQueries` 처리

## 코드 품질 기준

- 코드 생성 시 `code-review` 플러그인의 리뷰 기준(SOLID, React, TypeScript, React Hook Form, React Query 등 15개 카테고리)을 준수하도록 작성한다.
- 상세 기준은 code-review 플러그인 참조.

## React Performance Best Practices

Vercel 엔지니어링 기반 React/Next.js 성능 최적화 규칙. 각 규칙은 `skills/` 디렉토리에 개별 파일로 관리된다.

- **Async (CRITICAL)**: defer-await, parallel-promises, suspense-boundaries
- **Re-render (MEDIUM)**: memo-extract, memo-default-value, narrow-dependencies, derived-state, derived-state-no-effect, functional-setstate, lazy-state-init, simple-expression-memo, move-effect-to-event, transitions, useref-transient
- **Rendering (MEDIUM)**: conditional-render
- **JS (LOW-MEDIUM)**: index-maps, cache-property-access, length-check-first, early-exit, hoist-regexp, set-map-lookups, tosorted-immutable
- **Advanced (LOW)**: event-handler-refs
