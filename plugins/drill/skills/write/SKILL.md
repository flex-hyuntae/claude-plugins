---
name: write
description: 'Linear 티켓을 받아 연결된 Spec/Concept와 구현 가이드를 로드하고 코드를 작성한다. 사용자가 "/drill:write", "이 티켓 구현해줘", "티켓 작성", Linear URL과 함께 "코드 짜줘"를 요청할 때 트리거. 한 번에 티켓 1개만 처리. rules 플러그인이 설치되어 있으면 rules:write가 자동 적용된다. drill 워크플로우 세 번째 단계.'
compatibility: 'Linear MCP 필수. rules 플러그인 권장.'
disable-model-invocation: true
argument-hint: "[linear-issue-url|issue-id]"
---

# Write

Linear 티켓 하나를 받아 Spec/Concept + 구현 가이드로 코드 작성. rules 규칙은 `rules:write` 스킬이 자동 적용 (rules 플러그인 필요).

## Layer 경계 — Ticket = Single Source

**write 단계 = 티켓의 how 결정을 그대로 구현**. 단계별 질문 차원·원칙은 `plan` skill `§Layer 경계` 참고. spec/concept 은 도메인 어휘·책임 경계 참조용일 뿐 write 단계에서 재해석하지 않는다.

### write 단계 자의 결정 금지

티켓 본문의 §수용 기준 / §구현 가이드 / §코드 위치 가 결정해야 할 how 항목 — write 가 임의로 정하지 않는다:

- **UI 구체화** — 노출 매체·위치 (Dropdown / Popover / Toast / Modal / Sheet) / 선택지 우선순위 / 동일 행위 중복 처리
- **카탈로그 항목** — Dropdown 항목 / 메뉴 액션 N 개 등 구체 카탈로그
- **시그니처·카피·가드** — 컴포넌트 prop 분기 / CTA 라벨 / 권한별 disabled vs 비노출

### 티켓에 모호성이 남아있으면 → Cascade

티켓 본문을 읽었는데 위 항목 중 하나라도 결정 안 됨 / "미정" 으로 남아있음 / 명시 없음:

1. **write 단계에서 자의 결정 금지**
2. AskUserQuestion 으로 사용자에게 확인 — 단순 결정이면 즉시 닫고 진행 + 티켓 본문 업데이트(`save_issue`)
3. spec/concept 의 모호성과 얽혀있어 큰 결정이면 → **`/drill:prepare` 강화 모드로 cascade** (티켓 본문 재정합 후 write 재개)
4. 임시 코드 작성 후 "나중에 정하자" 식 진행 금지 — 모호성을 코드로 흡수하지 않는다

## Workflow

### 1. 컨텍스트 로드

1. `mcp__linear-server__get_issue` 로 티켓
2. description 에서 관련 Concept 경로 추출 → Spec index + Concept 파일 로드 (**도메인 어휘·책임 경계 참조용**)
3. 확인: 목표 / 수용 기준 / 구현 가이드 / 코드 위치
4. **Layer 점검** — 티켓 본문이 §Layer 경계 의 결정 차원(위치·매체·옵션·시그니처·중복·카피·가드)을 모두 닫고 있는지 확인. 결정 안 됨 항목 있으면 Cascade 절차로

### 2. 코드베이스 탐색 (인터랙티브)

Glob/Grep으로 관련 파일 → 핵심 파일 Read → 기존 패턴·유틸 재사용 판단.

적절한 위치를 찾을 때까지 AskUserQuestion 반복:
- 컴포넌트/로직/타입 추가 위치 (티켓의 §코드 위치 가 명확하면 생략 가능)
- 기존 재사용 vs 신규 생성

### 3. 코드 작성 (반복)

수용 기준을 하나씩 충족:
1. **티켓의 §수용 기준 = single source of truth** — Concept 으로 거슬러 올라가서 재해석하지 않는다
2. **티켓의 §구현 가이드·§코드 위치** 의 결정을 그대로 따른다
3. `rules:write` 자동 적용 (직접 로드 안 함)
4. 충족 중 layer 결정이 빠진 게 드러나면 즉시 멈추고 §Cascade 절차

**작업 단위 완료 후 AskUserQuestion**: "커밋 / 이어서 진행".

### 4. 검증

```bash
yarn turbo run type-check --filter=@flex-apps/{pkg}
yarn turbo run lint --filter=@flex-apps/{pkg}
```

에러 수정 후 재검증.

### 5. 완료

변경 파일 목록 + 수용 기준 충족 체크리스트. drill state 업데이트 (오케스트레이션 시).

## 제약

- 한 번에 티켓 1개만
- 한국어, 코드 위치·커밋 지속 확인
- **티켓 본문이 single source** — spec/concept 으로 거슬러 올라가 자의 재해석 금지
- **모호성을 코드로 흡수 금지** — 결정 빠진 항목 발견 시 §Cascade

## 에러

- 티켓 조회 실패 → URL/ID 재확인
- Spec/Concept 없음 → 티켓 정보만으로 진행 또는 `/drill:plan` 안내
- type-check/lint 실패 → 수정 후 재검증
- **티켓 본문에 layer 결정 빠짐** (위치/매체/옵션/시그니처/중복/카피/가드) → §Cascade — 단순 결정은 AskUserQuestion + `save_issue` 로 닫고 진행 / 큰 결정은 `/drill:prepare` 강화 모드로 cascade
