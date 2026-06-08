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

티켓 §수용 기준 / §구현 설계 가 결정해야 할 항목 — write 가 임의로 정하지 않는다:

- **제품 how** — 노출 매체·위치 (Dropdown / Popover / Toast / Modal / Sheet) / 선택지 우선순위 / 동일 행위 중복 / 카탈로그 항목 / prop 분기 / CTA 라벨 / 권한별 disabled vs 비노출
- **구현 how** — 변경 파일(신규/수정) / 함수·타입 시그니처 / 따라야 할 기존 패턴 / 재사용 vs 신규 / 레이어 배치

### 티켓에 모호성이 남아있으면 → Cascade

티켓 §구현 설계를 읽었는데 위 항목 중 하나라도 결정 안 됨 / "미정" / 명시 없음:

1. **write 단계에서 자의 결정 금지** — 파악을 위한 탐색은 가능하나 그 결과로 모호성을 임의 확정하지 않는다
2. AskUserQuestion 으로 사용자에게 확인 — 단순 결정이면 즉시 닫고 진행 + 티켓 본문 업데이트(`save_issue`)
3. spec/concept 의 모호성과 얽혀있거나 구현 설계가 통째로 비었으면 → **`/drill:prepare` 강화 모드로 cascade** (티켓 본문 재정합 후 write 재개)
4. 임시 코드 작성 후 "나중에 정하자" 식 진행 금지 — 모호성을 코드로 흡수하지 않는다

## Workflow

### 1. 컨텍스트 로드

1. `mcp__linear-server__get_issue` 로 티켓
2. description 에서 관련 Concept 경로 추출 → Spec index + Concept 파일 로드 (**도메인 어휘·책임 경계 참조용**)
3. 확인: 목표 / 수용 기준 / §구현 설계(변경 파일·시그니처·기존 패턴·재사용·변경 명세)
4. **Layer 점검** — §구현 설계가 §Layer 경계의 제품 how + 구현 how 를 모두 닫고 있는지 확인. 결정 안 됨 항목 있으면 Cascade 절차로

### 2. 구현 설계 ↔ 현재 코드 형상 대조 (작성 전 필수)

prepare 가 티켓을 쓴 시점과 write 시점 사이에 **코드 형상이 바뀌었을 수 있다**(다른 PR 머지·리팩터 등). 작성 전 **반드시 현재 형상 기준으로 티켓 §구현 설계를 재검증** — 기본은 탐색 없이 검증만:

- §구현 설계가 가리킨 변경 파일·기존 패턴 포인터(`file:line`)를 열어 **현재 코드가 설계와 일치하는지 확인** (파일 이동·심볼 변경·시그니처 변동·패턴 소멸·재사용 대상 변화 점검)
- §의존의 `blockedBy` 티켓 산출물이 실제로 머지됐는지·시그니처가 설계와 같은지 확인 — 다르면 §Cascade
- 어긋남 발견 → 자의 보정 금지, §Cascade (단순하면 AskUserQuestion + `save_issue`, 크면 prepare 강화)
- §구현 설계가 비어 있거나 "미정" → 임의로 메우지 말고 §Cascade
- **부족해서 탐색·판단이 불가피하면** 그 결과를 코드에만 남기지 말고 **prepare 강화로 환류**해 티켓을 single source 로 유지 (다음 사람도 같은 결과)

### 3. 코드 작성 (반복)

수용 기준을 하나씩 충족:
1. **티켓의 §수용 기준 = single source of truth** — Concept 으로 거슬러 올라가서 재해석하지 않는다
2. **티켓의 §구현 설계**(변경 파일·시그니처·기존 패턴·변경 명세) 를 그대로 따른다 — rules 규칙에 맞춰 작성
3. `rules:write` 자동 적용 (직접 로드 안 함)
4. 충족 중 설계가 빠진 게 드러나면 즉시 멈추고 §Cascade 절차

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

- 한 번에 티켓 1개만
- 한국어, 커밋 지속 확인
- **티켓 §구현 설계가 single source** — spec/concept 으로 거슬러 올라가 자의 재해석 금지. 탐색·판단이 필요하면 결과를 코드에만 남기지 말고 prepare 강화로 환류
- **모호성을 코드로 흡수 금지** — 결정 빠진 항목 발견 시 §Cascade

## 에러

- 티켓 조회 실패 → URL/ID 재확인
- Spec/Concept 없음 → 티켓 정보만으로 진행 또는 `/drill:plan` 안내
- type-check/lint 실패 → 수정 후 재검증
- **티켓 §구현 설계 빠짐/미정** (제품 how 또는 구현 how) → §Cascade — 단순 결정은 AskUserQuestion + `save_issue` 로 닫고 진행 / 큰 결정·통째 누락은 `/drill:prepare` 강화 모드로 cascade
