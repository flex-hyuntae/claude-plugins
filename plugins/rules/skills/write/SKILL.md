---
name: write
description: '코드를 작성·수정·리팩토링할 때 rules 플러그인에 정의된 규칙(React 컴포넌트, TypeScript, 스타일링, 프로젝트 구조, 접근성, 테스트, 네이밍, flex 컨벤션)을 참조한다. Edit/Write 직전 자동 트리거해서 카테고리별 규칙 파일을 로드한 뒤 코드를 생성한다. 작업 대상 카테고리는 매핑 표 기반으로 판단 — 여러 카테고리가 겹치면 모두 로드. typescript/ts-no-any, ts-no-type-assertion, naming/naming-conventions은 항상 적용.'
disable-model-invocation: false
---

# Rules 적용

코드를 작성·수정·리팩토링할 때 이 스킬이 트리거된다. 작업 대상 코드에 해당하는 카테고리의 규칙 파일을 읽고, 규칙을 준수하는 코드를 생성한다.

## 카테고리 매핑

작업 대상에 따라 해당 카테고리의 규칙 파일을 읽는다:

| 작업 대상 | 카테고리 디렉토리 | 규칙 수 |
|-----------|-------------------|---------|
| React 컴포넌트, 훅, 이벤트 핸들러 | `react/` | 24 |
| TypeScript 타입 정의, 제네릭 | `typescript/` | 3 |
| 디렉토리 구조, 도메인 설계 | `structure/` | 3 |
| vanilla-extract, 디자인 토큰 | `styling/` | 2 |
| 시맨틱 HTML, ARIA, 키보드 | `accessibility/` | 1 |
| 테스트 코드 | `testing/` | 1 |
| 네이밍, i18n 키 | `naming/` | 1 |
| flex 프로젝트 내부 컨벤션 (React Query Suspense, Modal 등) | `flex/` | 2 |

## 절차

1. 작업 대상 코드가 어떤 카테고리에 해당하는지 판단
2. 해당 카테고리 디렉토리의 규칙 파일을 읽음 (복수 카테고리 가능)
3. 규칙을 준수하여 코드를 작성
4. 위반 사항이 있으면 수정

## 항상 적용하는 규칙

어떤 코드를 작성하든 다음은 항상 확인:

- `typescript/ts-no-any.md` — any 타입 금지
- `typescript/ts-no-type-assertion.md` — as, ! 단언 금지
- `naming/naming-conventions.md` — 네이밍 컨벤션
