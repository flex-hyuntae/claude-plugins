---
name: write
description: 'Linear 티켓을 받아 연결된 Spec/Concept와 §구현 설계를 로드하고 rules 따라 코드를 작성한다. 사용자가 "/drill:write", "이 티켓 구현해줘", "티켓 작성", Linear URL과 함께 "코드 짜줘"를 요청할 때 트리거. 한 번에 티켓 1개만 처리. rules 플러그인이 설치되어 있으면 rules:write가 자동 적용된다. drill 워크플로우 세 번째 단계.'
compatibility: 'Linear MCP 필수. rules 플러그인 권장.'
disable-model-invocation: true
argument-hint: "[linear-issue-url|issue-id]"
---

# Write

Linear 티켓 하나를 받아 Spec/Concept + §구현 설계로 코드 작성. rules 규칙은 `rules:write` 스킬이 자동 적용 (rules 플러그인 필요).

## Layer 경계 — Ticket = Single Source

**write = 티켓 §구현 설계를 rules 따라 코드로 작성.** 티켓이 곧 구현 설계서이고, 설계는 prepare 에서 완성돼 있는 것이 기본 기대다. spec/concept 은 도메인 어휘·책임 경계 참조용일 뿐 재해석하지 않는다. 단계별 질문 차원은 `plan` skill `§Layer 경계`.

### Cascade — 미결을 코드로 흡수하지 않는다

티켓 §수용 기준 / §구현 설계 가 닫아야 할 항목(제품 how · 구현 how — `prepare` skill `§Layer 경계`) 이 결정 안 됨 / "미정" / 명시 없음이면:

1. **자의 결정 금지** — 파악을 위한 탐색은 하되 그 결과로 모호성을 임의 확정하지 않는다. 임시 코드 후 "나중에 정하자" 도 금지
2. 단순 결정 → AskUserQuestion 으로 닫고 진행 + `save_issue` 로 티켓에 반영
3. spec/concept 모호성과 얽혔거나 구현 설계가 통째로 비었으면 → `/drill:prepare` 강화 모드 (티켓 재정합 후 write 재개)

## 의존 방향 — 바깥 → 안 단방향

휘발성 바깥은 안정 코어에 **안정 인터페이스로만** 의존하고 역방향은 금지. stack 별 대응은 `references/STACK.md` §의존 방향.

경계는 모듈·컴포넌트가 아니라 **인터페이스**다 — colocate 자체는 정상이고 금지 대상은 **외부 형태가 코어로 새는 것**(raw 서버 응답이 표현까지 그대로 흐르는 등). 경계에서 변환해 어느 쪽이 바뀌어도 상대가 불변이어야 한다. §구현 설계의 레이어 배치를 그대로 따르고, 설계가 강결합으로 몰면 design smell → §Cascade.

## Workflow

### 1. 컨텍스트 로드

1. `mcp__linear-server__get_issue` 로 티켓
2. description 에서 관련 Concept 경로 추출 → Spec index + Concept 파일 로드 (**도메인 어휘·책임 경계 참조용**)
3. 확인: 목표 / 수용 기준 / §구현 설계(변경 파일·시그니처·기존 패턴·재사용·변경 명세). 제품 how + 구현 how 가 다 닫혀 있는지 점검 — 미결이면 §Cascade
4. **BE 레포면** `backend-guidelines-doc-loader` 로 컨벤션 문서 로드 (`references/STACK.md` §BE 컨벤션 위임)

### 2. 구현 설계 ↔ 현재 코드 형상 대조 (작성 전 필수)

prepare 시점과 write 시점 사이 코드가 바뀌었을 수 있다. §구현 설계의 변경 파일·기존 패턴 포인터(`file:line`)와 §의존 `blockedBy` 산출물(머지 여부·시그니처)이 현재 코드와 맞는지 검증한다 (탐색 없이 검증만).

어긋남 / 비어 있음 / "미정" → 자의 보정 금지, §Cascade. 탐색·판단이 불가피했으면 결과를 코드에만 남기지 말고 티켓에 환류(티켓이 single source).

### 3. 코드 작성 (반복)

수용 기준을 하나씩 충족 — **티켓 §수용 기준·§구현 설계가 single source**(Concept 으로 거슬러 재해석 금지), §의존 방향 유지, `rules:write` 자동 적용. 설계가 빠진 게 드러나면 즉시 멈추고 §Cascade.

**작업 단위 완료 후 AskUserQuestion**: "커밋 / 이어서 진행".

### 4. 검증

stack 별 커맨드는 `references/STACK.md` §검증. 에러 수정 후 재검증.

### 5. 완료

- 변경 파일 목록 + 수용 기준 충족 체크리스트
- **SoT 점검**: 티켓에 없던 결정이 생겼으면 `save_issue` 로 §구현 설계에 반영 — 티켓이 늘 single source 여야 다음 사람도 같은 결과
- drill state 업데이트 (오케스트레이션 시)

## 제약

- 한 번에 티켓 1개만 · 한국어 · 커밋 지속 확인
- 티켓 §구현 설계가 single source, 모호성을 코드로 흡수 금지 → 미결은 §Cascade

## 에러

- 티켓 조회 실패 → URL/ID 재확인
- Spec/Concept 없음 → 티켓 정보만으로 진행 또는 `/drill:plan` 안내
- type-check/lint 실패 → 수정 후 재검증
- §구현 설계 빠짐/미정 → §Cascade
