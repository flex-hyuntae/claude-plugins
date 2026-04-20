---
name: drill
description: plan → prepare → write → review → qa 워크플로우를 오케스트레이션합니다
disable-model-invocation: true
argument-hint: "[feature-name|resume]"
---

# Drill

plan → prepare → write → review → qa 워크플로우 오케스트레이션. 각 단계 완료 상태 추적 + 이어하기(resume) 지원. 각 하위 스킬은 단독 실행 가능.

## 워크플로우

```
/drill:drill {feature}
  → /drill:plan              → {FEATURE-NAME}.md + concepts/
  → /drill:prepare           → Linear 티켓 생성
  → /drill:write {ticket}    → 티켓 기반 코드 작성
  → /drill:review {feat} {pr} → Spec 동기화 + Decision Log
  → /drill:qa                → TC 작성
```

## 상태 추적

`~/Projects/flex/til/spec/{feature}/.drill-state.json`:

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
| 없음 | `til/spec/*/.drill-state.json` 스캔 → 진행 중 목록 AskUserQuestion |
| `{feature}` (신규) | 디렉토리·state 확인 후 Phase 1부터 |
| `{feature}` (기존) 또는 `resume` | state 기준 이어할 단계 AskUserQuestion |

### 단계 전환

각 단계 완료 후 state 업데이트 + 다음 단계 안내 (진행/건너뛰기 AskUserQuestion). 건너뛴 단계는 `skipped`.

**write 단계**: prepare 완료 후 "티켓 선택해 `/drill:write {ticket-id}` 실행" 안내. drill이 티켓 루프를 직접 돌리지 않음.

## 개별 스킬 독립 사용

모든 하위 스킬은 `/drill:plan`, `/drill:prepare {feature}` 등으로 단독 실행 가능. state 파일 있으면 자동 업데이트.

## 제약

- 한국어
- 각 단계 건너뛰기 가능 (비강제)
- state로 진행 추적, 순서·반복 실행 유연
