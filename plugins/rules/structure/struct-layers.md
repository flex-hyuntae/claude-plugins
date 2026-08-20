---
title: router · pages · domains · common 네 층
impact: HIGH
impactDescription: 참조 방향을 한 방향으로 고정
tags: structure, router, pages, domains, common, directory, fsd
---

## router · pages · domains · common 네 층

최상위는 이 넷이다. 다른 최상위 층을 만들지 않는다.

```
src/
├── router/     # 라우트 트리 — 페이지를 안다
├── pages/      # 라우트 진입점 — 도메인을 조합한다
├── domains/    # 비즈니스 도메인
└── common/     # 도메인을 모르는 것들
```

참조는 위에서 아래로만 흐른다. `router → pages → domains → common`. 역방향은 없고, 도메인끼리도 참조하지 않는다. 꼭 필요한 예외는 `x/` 창구로 연다 (→ `struct-domain-cross-import.md`).

### router — 라우트 트리

path 와 페이지를 잇는다. 라우트 정의, lazy import, 가드가 여기 있다.

```
router/
├── index.tsx          # 라우트 트리
└── guards/            # 인증 · 권한 가드
```

router 가 최상위인 이유는 페이지를 import 해야 하기 때문이다. `common/router` 로 두면 맨 아래층이 맨 위층을 알게 되어 방향이 역류한다.

path 문자열 상수는 반대로 페이지도 쓴다. 그건 `common/routes/` 에 둔다 — 문자열뿐이라 도메인도 페이지도 모른다.

`<Outlet />` 을 품은 껍데기는 router 것이 아니다. 탭 목록과 제목을 아는 컴포넌트라서 페이지다.

### pages — 진입점

라우트 하나가 폴더 하나다. 이름은 `XxxPage` 로 끝난다. 페이지는 도메인을 가져다 조합하는 자리이고, 도메인을 대신 정의하지 않는다.

라우트가 중첩되면 세그먼트를 소문자 폴더로 두고 그 안에 페이지를 넣는다. 그룹 폴더는 `index.tsx` 를 갖지 않는다.

```
pages/
├── UserListPage/
└── settings/
    ├── SettingsPage/       # /settings — 탭 + <Outlet />
    ├── ProfilePage/        # /settings/profile
    └── SecurityPage/       # /settings/security
```

라우트에 걸리는 컴포넌트는 껍데기든 잎이든 다 페이지다. 도메인 쪽과 다르게 페이지는 이런 그룹 폴더를 가진다 (→ `struct-no-fractal.md`).

페이지 하위는 평평하게 시작한다. 도메인으로 묶기 애매하면서 그 페이지에서만 쓰이는 것이 생기면 그때 폴더를 만든다.

```
pages/UserDetailPage/
├── index.tsx
├── style.css.ts
├── components/        # 이 페이지에서만 쓰는 컴포넌트
├── hooks/
├── queries/           # 이 페이지에서만 쓰는 조합 쿼리
├── models/            # 여러 도메인 model 을 합친 결과
└── parsers/
```

여러 도메인을 합치는 코드는 여기 말고 갈 곳이 없다. 페이지 폴더가 생기는 가장 흔한 이유가 이것이다.

### domains — 도메인별 응집

도메인 이름 그대로 폴더를 만든다. `UserDomain` 처럼 접미사를 붙이지 않는다. 자주 쓰는 하위 폴더는 여섯 개다.

| 폴더 | 담는 것 |
|---|---|
| `components/` | 도메인 컴포넌트 |
| `queries/` | query · mutation option 팩토리 (→ `struct-queries-module.md`) |
| `hooks/` | 도메인 훅 |
| `utils/` | 순수 함수 |
| `models/` | 타입 |
| `parsers/` | 타입 간 변환 (→ `struct-file-naming.md`) |
| `i18n/` | 그 도메인의 번역 키 |
| `x/` | 다른 도메인에게 열어 준 창구 (→ `struct-domain-cross-import.md`) |

여섯 개가 정해진 목록은 아니다. 안 쓰는 폴더는 만들지 않고, 필요하면 `stores/` 처럼 추가한다. 새로 만들 폴더가 이 여섯 중 하나로 이미 설명되는지만 확인한다.

무게는 도메인 쪽에 있다. 도메인이 두껍고 페이지는 그것을 조합해 배치하는 얇은 층이기를 기대한다. 페이지가 두꺼워지면 도메인으로 갈 것이 안 갔다는 신호다. 도메인을 언제 만드느냐에 정해진 시점은 없다.

이 폴더들은 도메인 루트에만 있다. 도메인 안에서 같은 구조가 다시 반복되지 않는다 (→ `struct-no-fractal.md`).

### common — 도메인을 모르는 것들

도메인 이름을 하나라도 알아야 한다면 common 이 아니다. 관심사별로 폴더를 나눈다.

```
common/
├── design-system/     # Button, Modal, Table
├── axios/             # instance, interceptor, 생성된 API 클라이언트
├── react-query/       # queryClient, 기본 option
├── routes/            # path 문자열 상수
└── utils/             # formatDate 같은 도메인 무관 함수
```

기준은 도메인 무관 하나뿐이다. 여러 화면에서 쓰인다는 것은 기준이 아니다. 권한·알림·파일 업로드처럼 어디서나 쓰이지만 자기 데이터와 화면을 가진 것은 도메인이다. 그 판단을 흐리면 common 이 두 번째 쓰레기통이 된다.

`common/design-system` 을 `domains/design-system` 으로 두고 싶어지지만 그러면 도메인이 도메인을 참조하게 되고, 참조 방향 규칙이 첫날 깨진다. 도메인이 쓰는 것은 도메인이 아니다.

common 하위는 도메인 규약을 그대로 따른다 — `components/`, `hooks/`, `utils/` 를 쓰고 프랙탈은 없다.
