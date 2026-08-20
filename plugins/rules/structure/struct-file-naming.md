---
title: 파일 배치와 파일명
impact: MEDIUM
impactDescription: 폴더만 보고 무엇이 들어있는지 알게 함
tags: structure, naming, file, parsers
---

## 파일 배치와 파일명

컴포넌트만 폴더를 가진다. 나머지는 폴더 아래 파일 하나다.

| 종류 | 경로 | 예 |
|---|---|---|
| 컴포넌트 | `components/Xxx/index.tsx` + `style.css.ts` | `components/UserCard/index.tsx` |
| 훅 | `hooks/useXxx.ts` | `hooks/useUserFilter.ts` |
| 유틸 | `utils/kebab-case.ts` | `utils/format-user-name.ts` |
| 타입 | `models/model-xxx.ts` | `models/model-user.ts` |
| 파서 | `parsers/xxx-to-yyy.ts` | `parsers/user-to-user-option.ts` |
| 쿼리 | `queries/xxxQueries.ts` | `queries/searchUserQueries.ts` |

훅과 쿼리는 export 이름이 곧 파일명이라 camelCase 다. 유틸·타입·파서는 kebab-case 파일에 함수를 담는다.

컴포넌트만 폴더를 가지는데 그 폴더도 두 파일에서 끝난다 (→ `struct-no-fractal.md`).

테스트와 스토리는 대상 파일의 형제로 둔다 — `index.test.tsx`, `format-user-name.test.ts`. `__tests__/` 폴더를 만들지 않는다.

barrel 파일은 만들지 않는다. `domains/user/index.ts` 로 도메인을 한꺼번에 열면 `x` 창구가 의미를 잃는다. 유일한 예외가 `x/*.ts` 다 (→ `struct-domain-cross-import.md`).

### parsers 는 AToB

변환 함수는 무엇을 무엇으로 바꾸는지 이름에 다 드러낸다. `parse`, `convert`, `transform` 같은 접두사는 쓰지 않는다.

```ts
// ❌
export function parseUser(dto: UserDto): User {}
export function convertToOption(user: User): SelectOption {}

// ✅ parsers/user-to-select-option.ts
export function userToSelectOption(user: User): SelectOption {}
export function selectOptionToUser(option: SelectOption): User {}
```

파일 하나에 파서 몇 개가 들어가도 된다. 같은 타입 쌍을 다루는 변환은 한 파일에 모은다.
