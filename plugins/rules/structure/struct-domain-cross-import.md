---
title: 도메인 격리와 x 창구
impact: HIGH
impactDescription: 도메인 간 참조를 막고, 예외는 폴더로 드러냄
tags: structure, domains, dependency, cross-import, public-api
---

## 도메인 격리와 x 창구

도메인은 서로를 참조하지 않는다. 엮이는 일은 페이지에서 한다 (→ `struct-layers.md`).

그래도 꼭 필요한 자리가 나온다. 그럴 때 참조를 몰래 열지 않고 창구를 만든다. 쓰는 도메인 이름으로 파일을 하나 두고, 소비하는 쪽은 그 파일만 import 한다.

```
domains/user/
├── components/UserAvatar/
├── models/model-user-view.ts
├── queries/searchUserQueries.ts
└── x/
    ├── review.ts        # review 에게 열어 준 창구
    └── goal.ts          # goal 에게 열어 준 창구
```

```ts
// domains/user/x/review.ts
export { UserAvatar } from '../components/UserAvatar';
export { searchUserQueries } from '../queries/searchUserQueries';
export type { UserView } from '../models/model-user-view';

// domains/review/components/ReviewFeed/index.tsx
import { UserAvatar, type UserView } from '@/domains/user/x/review';
```

창구를 열기로 했으면 무엇을 열지는 제한하지 않는다. `components` · `models` · `queries` · `hooks` 전부 열 수 있다. 반만 열면 소비하는 쪽이 우회로를 만들고, 그 우회로는 폴더에 안 남는다.

폴더 이름은 `x` 다. 짧아서 경로에서 눈에 걸리고 정렬상 아래로 밀린다.

### x 는 예외를 세는 자리다

`x` 는 참조를 편하게 하는 장치가 아니라 예외를 코드에 남기는 장치다. `user/x/` 에 파일이 늘어나면 격리가 그만큼 무너진 것이고, 폴더를 열면 그 개수가 바로 보인다.

도메인 사이에도 층이 있다. 로그인한 사용자처럼 다른 도메인들이 딛고 서는 기반 도메인은 `x` 파일이 여러 개 생기는 것이 정상이다. 개수가 아니라 방향이 한쪽인지를 본다.

`x` 없이 직접 import 를 허용하면 같은 일이 벌어지는데도 어디에도 안 드러난다. 도메인 하나를 지울 때 무엇이 깨지는지 grep 으로 세야 한다.

### x 는 자기 도메인 재수출만 담는다

`x/*.ts` 에는 상대 경로 재수출만 있다. `x` 파일끼리는 서로를 참조하지 않는다.

### 먼저 복제를 본다

창구를 열기 전에 복제로 끝나는지 확인한다. `review` 가 아는 작성자가 `{ id, name }` 뿐이면 자기 `models/` 에 그렇게 적는다. 이름이 같다고 타입을 하나로 모으면 그 타입이 두 도메인의 요구를 동시에 진다.

### 페이지는 x 를 거치지 않는다

페이지는 위층이라 도메인 내부를 그대로 import 한다. `x` 는 도메인끼리만 쓰는 장치다.

여러 도메인을 합친 타입은 페이지 하위 `models/` 에 둔다. 합치는 함수도 같은 페이지 `parsers/` 다.
