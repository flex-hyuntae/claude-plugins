---
title: 도메인 안에서 구조를 반복하지 않는다
impact: HIGH
impactDescription: 도메인 내부 깊이를 두 단계로 고정
tags: structure, component, domains, fractal
---

## 도메인 안에서 구조를 반복하지 않는다

컴포넌트 폴더는 두 파일로 끝난다.

```
components/UserCard/
├── index.tsx
└── style.css.ts
```

컴포넌트 하위에 `components/` · `hooks/` · `queries/` 를 다시 만들지 않는다. 도메인 안에서 같은 구조가 반복되면 어떤 것이 도메인 것이고 어떤 것이 한 컴포넌트 것인지 경로 깊이로만 갈리게 된다. 깊이는 경계가 아니다.

```
// ❌ 도메인 안에서 구조가 반복된다
domains/user/components/UserCard/
├── index.tsx
├── components/UserCardBadge/
└── hooks/useUserCardState.ts

// ✅ 도메인 폴더에 형제로 둔다
domains/user/
├── components/UserCard/
├── components/UserCardBadge/
└── hooks/useUserCardState.ts
```

한 컴포넌트만 쓰는 훅이라도 도메인 `hooks/` 에 둔다. 쓰는 곳이 하나인지는 파일 위치가 아니라 import 를 보면 안다.

### 예외 — 페이지

`pages/XxxPage/` 는 하위 폴더를 가진다 (→ `struct-layers.md`). 페이지는 조합 지점이라 도메인으로 묶기 애매한 것들이 모이고, 라우트당 하나뿐이라 반복되지 않는다.

컴포넌트가 커져서 쪼개고 싶어지면 하위 폴더가 아니라 도메인 형제로 뽑는다. 그래도 애매하면 그 컴포넌트가 실은 페이지 것이라는 신호다.
