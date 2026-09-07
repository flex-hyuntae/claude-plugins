---
name: qa
description: 'Spec/Concept/Decision Log/구현 코드를 종합해 QA 테스트 케이스(TC)를 작성한다. 사용자가 "$drill-codex:qa", "QA TC 만들어줘", "테스트 케이스 작성", "커버리지 매트릭스"를 요청할 때 트리거. TC 초안 작성은 drill-qa agent에 위임 — 이 skill은 입력 수집·사용자 리뷰·저장 담당. drill 워크플로우 마지막 단계.'
argument-hint: "[spec-feature-name]"
---

> **Codex 위임 규칙**: `drill-*` 분석 역할이 나오면 [Codex 하위 에이전트 위임](../../references/CODEX-DELEGATION.md)을 먼저 읽고 해당 역할 문서를 프롬프트로 사용한다.


# QA (Dispatcher)

TC 초안·커버리지 매트릭스 작성은 `drill-qa` agent에 위임. 이 skill은 입력 수집·사용자 리뷰·TC 저장 담당.

## Workflow

### 1. 입력 수집

**필수**: feature name — 인자 없으면 `ls ~/Projects/flex/wiki/Spec/` + 사용자 확인.

**선택 (사용자 확인 일괄)**: Figma URL / Linear project ID / feature flag. "없음" 기본.

### 2. Agent 호출

Codex 하위 에이전트 로 `drill-qa` 호출. prompt에 위 입력 + `code_root_hint`.

### 3. 리포트 분기

| 조건 | 처리 |
|------|------|
| `spec_missing: true` | `$drill-codex:plan` 선행 안내 후 종료 |
| `## Coverage Gaps` 누락 있음 | "보강 후 재실행(`$drill-codex:add-concept` 또는 `$drill-codex:plan`) / 일단 진행 / 취소" |
| 정상 | Phase 4 |

### 4. 사용자 리뷰

리포트 전체 표시 + 사용자 확인 — "저장 진행 / TC 수정 요청 / 취소".

수정 요청 시 사용자 피드백을 prompt에 포함해 agent 재호출.

### 5. 저장

사용자 확인으로 방식 선택:

- **Notion**: `mcp__notion__notion-create-pages({ parentPageUrl, pages: [{ title: "[{feature}] QA TC", content: 리포트 전체 }] })`. parent URL은 사용자 입력 또는 기본값.
- **로컬**: `~/Projects/flex/wiki/Spec/{feature}/TC.md` (`templates/TC.md` 형식). 필요 시 재구성.

### 6. 완료

저장 경로/Notion URL · 커버리지 매트릭스 요약 · 누락 항목 재안내.

## 제약

- 한국어
- TC 초안 작성·수정은 agent 재호출로 (skill이 TC 직접 수정 금지)

## 에러

- Spec 디렉토리 없음 → `$drill-codex:plan` 안내
- Figma/Linear 접근 불가 → agent가 자동으로 코드·spec 기반 진행 (`figma_used`/`linear_used: false`)
- Concept 책임·에지 부족 → Coverage Gaps 케이스
- Notion 저장 실패 → 로컬 저장 폴백 제안
