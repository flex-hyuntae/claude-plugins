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

**write 단계 = 티켓 §구현 설계를 rules 따라 코드로 작성**. 단계별 질문 차원·원칙은 `plan` skill `§Layer 경계` 참고. **티켓이 곧 구현 설계서** — 구현 설계는 prepare 에서 완성돼 있는 것이 기본 기대이고 write 는 작성에 집중한다. **단 티켓 내용이 부족하면** write 에서 탐색·판단이 필요할 수 있다 — 그때는 모호성을 코드로 흡수하지 말고 **§Cascade 로 prepare 에 환류**해 티켓을 강화한다. spec/concept 은 도메인 어휘·책임 경계 참조용일 뿐 재해석하지 않는다.

### write 단계 자의 결정 금지

티켓 §수용 기준 / §구현 설계 가 결정해야 할 항목(제품 how · 구현 how — `prepare` skill `§Layer 경계` 의 2 층 카탈로그) 을 write 가 임의로 정하지 않는다. 하나라도 미결이면 → §Cascade.

### 티켓에 모호성이 남아있으면 → Cascade

티켓 §구현 설계를 읽었는데 위 항목 중 하나라도 결정 안 됨 / "미정" / 명시 없음:

1. **write 단계에서 자의 결정 금지** — 파악을 위한 탐색은 가능하나 그 결과로 모호성을 임의 확정하지 않는다
2. AskUserQuestion 으로 사용자에게 확인 — 단순 결정이면 즉시 닫고 진행 + 티켓 본문 업데이트(`save_issue`)
3. spec/concept 의 모호성과 얽혀있거나 구현 설계가 통째로 비었으면 → **`/drill:prepare` 강화 모드로 cascade** (티켓 본문 재정합 후 write 재개)
4. 임시 코드 작성 후 "나중에 정하자" 식 진행 금지 — 모호성을 코드로 흡수하지 않는다

## 데이터 흐름 ↔ 표현 분리 (의존 방향)

**의존 방향을 고정**한다: 표현(마크업·스타일, 휘발성)은 데이터 흐름(조회·상태·뷰 모델·로직, 안정)에 **안정 인터페이스(뷰 모델/훅 반환/props)로만** 의존하고 역방향은 금지.

- 경계는 컴포넌트가 아니라 **인터페이스**다 — fetch 의 컴포넌트 colocate 는 정상. 금지 대상은 **서버 응답 형태가 표현으로 새는 것**: raw 응답을 경계에서 뷰 모델로 변환해 표현은 그 인터페이스만 본다 (응답·표현 어느 쪽이 바뀌어도 상대 불변)
- 티켓 `[플로우]`(데이터)/`[마크업]`(표현) 축 = 이 경계. §구현 설계의 레이어 배치를 그대로 따르고, 설계가 강결합으로 몰면 design smell → §Cascade

## Workflow

### 1. 컨텍스트 로드

1. `mcp__linear-server__get_issue` 로 티켓
2. description 에서 관련 Concept 경로 추출 → Spec index + Concept 파일 로드 (**도메인 어휘·책임 경계 참조용**)
3. 확인: 목표 / 수용 기준 / §구현 설계(변경 파일·시그니처·기존 패턴·재사용·변경 명세)
4. **Layer 점검** — §구현 설계가 §Layer 경계의 제품 how + 구현 how 를 모두 닫고 있는지 확인. 결정 안 됨 항목 있으면 Cascade 절차로

### 2. 구현 설계 ↔ 현재 코드 형상 대조 (작성 전 필수)

prepare 작성 시점과 write 시점 사이 코드 형상이 바뀌었을 수 있다. 작성 전 §구현 설계를 현재 형상 기준으로 재검증(탐색 없이 검증만):

- §구현 설계의 변경 파일·기존 패턴 포인터(`file:line`)와 §의존 `blockedBy` 산출물(머지 여부·시그니처)이 현재 코드와 일치하는지 확인
- 어긋남 / 비어 있음 / "미정" → 자의 보정·임의 메움 금지, §Cascade. 탐색·판단이 불가피했으면 결과를 코드에만 남기지 말고 §Cascade 로 환류(티켓이 single source)

### 3. 코드 작성 (반복)

수용 기준을 하나씩 충족 — **티켓 §수용 기준·§구현 설계가 single source**(Concept 으로 거슬러 재해석 금지), §데이터 흐름 ↔ 표현 분리 유지, `rules:write` 자동 적용. 설계가 빠진 게 드러나면 즉시 멈추고 §Cascade.

**작업 단위 완료 후 AskUserQuestion**: "커밋 / 이어서 진행".

### 4. 검증

```bash
yarn turbo run type-check --filter=@flex-apps/{pkg}
yarn turbo run lint --filter=@flex-apps/{pkg}
```

에러 수정 후 재검증.

### 5. 완료

- 변경 파일 목록 + 수용 기준 충족 체크리스트
- **SoT 점검**: 작업 중 탐색·판단으로 티켓에 없던 결정이 생겼으면 `save_issue` 로 티켓 §구현 설계에 반영 — **티켓이 늘 single source** 여야 다음 사람도 같은 결과 (코드에만 남기지 않는다)
- drill state 업데이트 (오케스트레이션 시)

## 제약

- 한 번에 티켓 1개만 · 한국어 · 커밋 지속 확인
- 티켓 §구현 설계가 single source, 모호성을 코드로 흡수 금지 → 미결은 §Cascade

## 에러

- 티켓 조회 실패 → URL/ID 재확인
- Spec/Concept 없음 → 티켓 정보만으로 진행 또는 `/drill:plan` 안내
- type-check/lint 실패 → 수정 후 재검증
- §구현 설계 빠짐/미정 → §Cascade
