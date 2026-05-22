---
title: DDD 기반 디렉토리 구조
impact: MEDIUM
impactDescription: 도메인별 응집도 향상
tags: structure, ddd, directory, domain
---

## DDD 기반 디렉토리 구조

기능(component)별이 아닌 도메인 단위로 묶는다.

```
<domain>/
├── api/        # query / mutation factory (→ flex/react-query-factory.md)
├── ui/         # 도메인 컴포넌트
├── lib/        # 훅 · 유틸 · store
└── model/      # 타입 · 파서
```

- queries / mutations 는 도메인 내 `api/` 에 모은다
- query factory 는 `{ baseQueryKey, options }` 패턴 (→ `flex/react-query-factory.md`)
- 도메인을 가로지르는 의존이 생기면 별도 도메인으로 추출
