---
name: review
description: PR과 연결된 Linear 티켓을 대조하고, 차이를 Ticket → Concept → Spec 순으로 cascade 업데이트하며 Decision Log를 작성합니다
disable-model-invocation: true
argument-hint: "[feature-name] [pr-url|pr-number]"
---

# Review (Dispatcher)

PR ↔ Ticket 차이 감지는 `drill-review` agent에 위임. 이 skill은 **사용자 확정·Linear 티켓 업데이트·Decision Log/Concept/Spec 파일 수정**을 담당한다.

원칙: 1차 비교 기준은 Ticket · cascade는 최소 범위부터 제안 · 모든 변경은 Decision Log에 기록 · 파일/티켓 수정 전 사용자 확정 필수.

## Workflow

### 1. 인자 파싱

- feature name 없으면 `ls ~/Projects/flex/til/spec/` + AskUserQuestion
- PR 식별자 없으면 "현재 브랜치 최신 PR"

### 2. Agent 호출

`Task` 로 `drill-review` 호출. prompt: `feature name: {...}\nPR 식별자: {...}`.

### 3. 리포트 분기

| 조건 | 처리 |
|------|------|
| `error: pr_fetch_failed` | PR 재입력 또는 종료 |
| `ticketless: true` | AskUserQuestion — "PR로 역 티켓 생성(`/drill:prepare`)" / "취소" |
| `spec_missing: true` | "`/drill:plan` 선행" / "Ticket만 진행(cascade=ticket_only 고정)" / "취소" |
| 차이 없음 | "PR과 티켓이 일치합니다" 출력 후 종료 |
| 차이 있음 | Phase 4 |

### 4. Diff 확정 인터뷰

각 Diff마다 순서대로 AskUserQuestion:

1. **차이 확인** (`needs_user_confirmation: true` 만): ticket_says ↔ pr_observation 보여주고 "맞음 / 아님(agent 오판) / 부분적으로 맞음"
2. **Cascade 레벨**: agent 추천을 기본값으로 — `ticket_only` / `ticket_concept` / `ticket_concept_spec` / "구현 누락(PR을 티켓에 맞춰 수정)" / "다른 티켓으로 이관" / "건너뛰기"
3. **변경 이유**: 자유 입력 → Decision Log `## 변경 이유` 에 그대로

트리거는 skill이 `PR #{번호} 리뷰` 로 자동 채움.

### 5. Ticketless Implementation

해당 섹션 항목마다 AskUserQuestion — "신규 티켓 생성(`/drill:prepare`) / 기존 티켓 편입(ID 입력 후 Phase 4 절차) / 범위 외 기록만 / 건너뛰기".

### 6. Cascade 실행

확정된 Diff별로 초안(ticket 수정 / Decision Log / Concept·Spec 수정)을 보여주고 "진행 / 건너뛰기 / 취소" 최종 확인 후 실행.

**레벨별 실행:**

- **공통 (모든 레벨)**:
  - `save_issue` 로 description 수정 — 수용 기준·구현 가이드 갱신 + 본문 하단 `## Decision Log` 섹션 누적 (`- [YYYY-MM-DD-NNN](경로) — 요약`)
  - `~/Projects/flex/til/spec/{feature}/decisions/YYYY-MM-DD-NNN.md` 작성 (`templates/DECISION.md` 기반, NNN은 같은 날짜 내 01부터)
- **`ticket_concept` 이상**:
  - 대상 Concept 파일 수정. 신규면 `concepts/{name}.md` 생성. 폐기면 `concepts/_archive/` 이동 + 상단 배너 삽입 + 타 concept의 참조 정리
- **`ticket_concept_spec`**:
  - SPEC.md Concepts 테이블·Concept 연결 리스트·Decision Log 테이블 갱신. 폐기된 concept은 `archived: [name](...)  — 사유 (YYYY-MM-DD)` 한 줄로

### 7. 완료 안내

업데이트된 티켓 URL · Decision Log 경로 · 수정된 Concept/Spec 파일 · 신규 티켓 필요 항목(`/drill:prepare` 안내).

## 제약

- 한국어
- 소스 코드 수정 금지. 티켓 description + spec/concept/decision 파일만 수정
- Phase 6 실행 전 diff 초안 사용자 확인 필수
- agent 재호출 가능 — PR 리뷰 중 새 변경이 생기면 skill 재호출 시 agent가 최신 PR을 다시 읽어 동일 cascade 수행

## 에러

- 티켓 `save_issue` 실패 → 수정용 description 텍스트 제공 후 수동 안내
- Decision Log 파일명 충돌 → NNN 증가 재시도
- Concept 새 이름이 `_archive/` 와 충돌 → 새 이름 AskUserQuestion
- 일부 티켓 조회 실패 → 실패분 제외 진행, 최종 안내에 목록 포함
