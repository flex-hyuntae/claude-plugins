---
name: drill
description: plan → prepare → review → qa 워크플로우를 오케스트레이션합니다
disable-model-invocation: true
argument-hint: "[feature-name|resume]"
---

# Drill

plan → prepare → write → review → qa 워크플로우를 연결하는 오케스트레이션 스킬입니다.
각 단계의 완료 상태를 추적하고, 이어하기(resume)를 지원합니다.

## 워크플로우

```
/drill:drill {feature}
   ↓
1. /drill:plan         → {FEATURE-NAME}.md + concepts/ 생성
   ↓
2. /drill:prepare      → Linear 티켓 생성
   ↓
3. /drill:write {ticket}  → 티켓 기반 Spec/Concept 참조 코드 작성
   ↓
4. /drill:review {feature} {pr}  → Spec 동기화 + Decision Log
   ↓
5. /drill:qa           → TC 작성
```

## 상태 추적

`~/Projects/flex/til/spec/{feature}/.drill-state.json`에 진행 상태를 저장합니다:

```json
{
  "feature": "job-grade-modal",
  "currentPhase": "plan",
  "phases": {
    "plan": { "status": "complete", "completedAt": "2026-03-27T10:00:00Z" },
    "prepare": { "status": "in-progress" },
    "write": { "status": "pending" },
    "review": { "status": "pending" },
    "qa": { "status": "pending" }
  },
  "specPath": "spec/job-grade-modal/"
}
```

**상태값:** `pending` | `in-progress` | `complete` | `skipped`

## 실행 로직

### 인자 없음 — 진행 중인 drill 목록

```
/drill:drill
```

`~/Projects/flex/til/spec/` 하위의 모든 `.drill-state.json`을 스캔하여 진행 중인 drill 목록을 표시합니다:

```
진행 중인 drill:

1. job-grade-modal — prepare (진행중)
   plan ✅ → prepare 🔄 → write ⏳ → review ⏳ → qa ⏳

2. markdown-animation — plan (완료)
   plan ✅ → prepare ⏳ → write ⏳ → review ⏳ → qa ⏳

어떤 drill을 이어할까요?
```

AskUserQuestion으로 선택하면 해당 feature의 다음 단계를 시작합니다.
진행 중인 drill이 없으면 새 feature name을 입력받습니다.

### 새로 시작

```
/drill:drill job-grade-modal
```

1. `spec/job-grade-modal/` 존재 확인
   - 없으면 → Phase 1(plan)부터 시작
   - 있으면 → `.drill-state.json` 확인
2. `.drill-state.json` 없으면 → Phase 1부터 시작
3. `.drill-state.json` 있으면 → 이어하기 제안

### 이어하기

```
/drill:drill resume
```

또는 feature name으로 재실행 시:

```
이전 진행 상태가 있습니다:
- plan: ✅ 완료
- prepare: ✅ 완료
- write: ⏳ 대기중
- review: ⏳ 대기중
- qa: ⏳ 대기중

어느 단계부터 이어할까요?
```

AskUserQuestion으로 시작 단계 선택.

### 단계 전환

각 단계 완료 후:
1. `.drill-state.json` 업데이트
2. 다음 단계 안내

```
✅ plan 단계 완료 — {FEATURE-NAME}.md + 3개 Concept 생성

다음 단계: prepare (Linear 티켓 생성)
진행할까요?
```

**write 단계 처리:**
prepare 완료 후:
```
✅ prepare 단계 완료 — 5개 티켓 생성

다음은 write 단계입니다.
/drill:write {ticket-id}로 티켓 기반 코드 작성을 시작하세요.
또는 /drill:drill resume로 이어할 수 있습니다.
```

### 단계 건너뛰기

```
review 단계를 건너뛰시겠습니까?
```

건너뛴 단계는 `skipped`로 기록.

## 개별 스킬 독립 사용

모든 하위 스킬은 독립적으로 사용 가능합니다:

```
/drill:plan                    # plan만 단독 실행
/drill:prepare job-grade-modal # prepare만 단독 실행
/drill:write CORE-1234         # write만 단독 실행
/drill:review job-grade-modal PR-URL  # review만 단독 실행
/drill:qa job-grade-modal      # qa만 단독 실행
```

독립 실행 시에도 `.drill-state.json`이 있으면 상태를 업데이트합니다.

## 중요 사항

- **언어**: 모든 커뮤니케이션은 한국어
- **비강제**: 각 단계는 건너뛸 수 있음
- **독립성**: 각 스킬은 drill 없이도 독립 실행 가능
- **상태 보존**: `.drill-state.json`으로 진행 상태 추적
- **유연성**: 순서를 바꾸거나 특정 단계만 반복 실행 가능
