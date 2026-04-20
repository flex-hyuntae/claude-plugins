---
name: qa
description: Spec, Concepts, Decision Log, 구현 코드를 기반으로 QA 테스트 케이스를 작성합니다
disable-model-invocation: true
argument-hint: "[spec-feature-name]"
---

# QA (Dispatcher)

TC 초안·커버리지 매트릭스 작성은 `drill-qa` agent에 위임. 이 skill은 입력 수집·사용자 리뷰·TC 저장 담당.

## Workflow

### 1. 입력 수집

**필수**: feature name — 인자 없으면 `ls ~/Projects/flex/til/spec/` + AskUserQuestion.

**선택 (AskUserQuestion 일괄)**: Figma URL / Linear project ID / feature flag. "없음" 기본.

### 2. Agent 호출

`Task` 로 `drill-qa` 호출. prompt에 위 입력 + `code_root_hint`.

### 3. 리포트 분기

| 조건 | 처리 |
|------|------|
| `spec_missing: true` | `/drill:plan` 선행 안내 후 종료 |
| `## Coverage Gaps` 누락 있음 | "보강 후 재실행(`/drill:add-concept` 또는 `/drill:plan`) / 일단 진행 / 취소" |
| 정상 | Phase 4 |

### 4. 사용자 리뷰

리포트 전체 표시 + AskUserQuestion — "저장 진행 / TC 수정 요청 / 취소".

수정 요청 시 사용자 피드백을 prompt에 포함해 agent 재호출.

### 5. 저장

AskUserQuestion으로 방식 선택:

- **Notion**: `mcp__notion__notion-create-pages({ parentPageUrl, pages: [{ title: "[{feature}] QA TC", content: 리포트 전체 }] })`. parent URL은 사용자 입력 또는 기본값.
- **로컬**: `~/Projects/flex/til/spec/{feature}/TC.md` (`templates/TC.md` 형식). 필요 시 재구성.

### 6. 완료

저장 경로/Notion URL · 커버리지 매트릭스 요약 · 누락 항목 재안내 · `/flex-workflow:run-qa` 안내.

## 제약

- 한국어
- agent는 읽기·분석만, 저장은 skill에서
- 사용자 피드백은 agent 재호출로 반영 (skill이 TC 직접 수정 금지)
- 저장 경로/페이지는 AskUserQuestion으로 최종 확인

## 에러

- Spec 디렉토리 없음 → `/drill:plan` 안내
- Figma/Linear 접근 불가 → agent가 자동으로 코드·spec 기반 진행 (`figma_used`/`linear_used: false`)
- Concept 책임·에지 부족 → Coverage Gaps 케이스
- Notion 저장 실패 → 로컬 저장 폴백 제안
