---
name: drill
description: 'plan → prepare → write → review → qa 워크플로우 전체를 오케스트레이션한다. 사용자가 "/drill", "$drill-codex:drill", "drill 시작", "전체 워크플로우 돌려줘", "feature 작업 시작"을 요청할 때 트리거. 각 단계 진행 상태를 추적하고 중간 이탈 시 resume 인자로 이어하기 가능. 각 하위 skill은 단독 실행도 지원.'
argument-hint: "[feature-name|resume]"
---

> **Codex 위임 규칙**: `drill-*` 분석 역할이 나오면 [Codex 하위 에이전트 위임](../../references/CODEX-DELEGATION.md)을 먼저 읽고 해당 역할 문서를 프롬프트로 사용한다.


# Drill

plan → prepare → write → review → qa 워크플로우 오케스트레이션. 각 단계 완료 상태 추적 + 이어하기(resume) 지원. 각 하위 스킬은 `$drill-codex:plan`, `$drill-codex:prepare {feature}` 처럼 단독 실행도 가능 (state 파일 있으면 자동 업데이트).

## 워크플로우

```
$drill-codex:drill {feature}
  → $drill-codex:plan                  → {FEATURE-NAME}.md + concepts/
  → $drill-codex:prepare               → Linear 티켓 생성
  → $drill-codex:write {ticket}        → 단일 티켓 구현
    또는
    $drill-codex:ship {ticket-ids}     → 의존 분석 + worktree + batch draft PR
  → $drill-codex:review {feat} {pr}    → Spec 동기화 + Decision Log
  → $drill-codex:qa                    → TC 작성
```

## 상태 추적

`~/Projects/flex/wiki/Spec/{feature}/.drill-state.json`:

```json
{
  "feature": "...",
  "currentPhase": "plan",
  "phases": {
    "plan":    { "status": "complete", "completedAt": "..." },
    "prepare": { "status": "in-progress" },
    "write":   { "status": "pending" },
    "review":  { "status": "pending" },
    "qa":      { "status": "pending" }
  }
}
```

상태값: `pending` / `in-progress` / `complete` / `skipped`.

## 실행

| 인자 | 동작 |
|------|------|
| 없음 | `til/spec/*/.drill-state.json` 스캔 → 진행 중 목록 사용자 확인 |
| `{feature}` (신규) | 디렉토리·state 확인 후 Phase 1부터 |
| `{feature}` (기존) 또는 `resume` | state 기준 이어할 단계 사용자 확인 |

### 단계 전환

각 단계 완료 후 state 업데이트 + 다음 단계 안내 (진행/건너뛰기 사용자 확인). 건너뛴 단계는 `skipped`.

**write 단계**: prepare 완료 후 두 가지 경로 안내:
- 단일 티켓: `$drill-codex:write {ticket-id}`
- 여러 티켓 batch (의존 순서대로 draft PR 일괄 생성): `$drill-codex:ship {ticket-ids}`

drill이 티켓 루프를 직접 돌리지 않음. ship 완료는 write phase `complete` 로 기록 (write/ship은 alternative — 둘 중 하나만 실행).

## 제약

- 한국어
- state로 진행 추적, 순서·반복 실행 유연 (각 단계 건너뛰기 비강제)
