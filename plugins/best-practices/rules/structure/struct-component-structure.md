---
title: 컴포넌트 폴더 구조
impact: MEDIUM
impactDescription: 일관된 프로젝트 구조 유지
tags: structure, component
---

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
