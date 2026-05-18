---
name: prepare
description: 'Spec/Concepts를 바탕으로 Linear 티켓을 생성하거나 기존 티켓을 강화한다. 사용자가 "/drill:prepare", "티켓 만들어줘", "Linear 티켓 생성", "티켓 보강", "스펙에서 티켓 발급"을 요청할 때 트리거. 인자가 spec feature 이름이면 생성 모드, Linear URL/ID면 강화 모드. drill 워크플로우의 두 번째 단계(plan 다음).'
compatibility: 'Linear MCP 필수'
disable-model-invocation: true
argument-hint: "[spec-feature-name|linear-issue-url|issue-id]"
---

# Prepare

Spec/Concepts 기반으로 Linear 티켓 **생성**하거나 기존 티켓 **강화**. 인자로 모드 자동 판단.

| 인자 | 모드 |
|------|------|
| feature name (`job-grade-modal`) | 생성 |
| Linear URL/ID (`CORE-1234`) | 강화 |
| 없음 | AskUserQuestion |

## Layer 경계 — Spec 모호성(what/why) → Ticket 구체화(how)

prepare 의 핵심 책임은 **spec/concept 의 의도된 모호성(what/why) 을 ticket 본문에서 구체화(how)** 하는 것. 단계별 질문 차원·원칙은 `plan` skill `§Layer 경계` 참고. **본 단계 = how 차원**, plan 에서 닫힌 what/why 는 재논의하지 않는다 (의문 시 plan 으로 cascade).

### Ticket 본문에 들어가야 할 7 구체화 차원

| 차원 | 예시 |
|------|------|
| 노출 매체·위치 | "AI 게시 셀 = Dropdown / OFF 시각 표식 = 제목 영역" |
| 선택지 우선순위 | "Footer paginator 의 size selector / navigator / count 중 본 사이클 = navigator 만" |
| 카탈로그 항목 | "Dropdown 항목 = ON / OFF" / "More 메뉴 = AI 게시 / 그룹 옮기기 / 삭제" |
| 동일 행위 중복 처리 | "다운로드: Callout + More 메뉴 둘 다 vs 하나만" |
| 컴포넌트 시그니처 | "props discriminated union { variant: 'single' \| 'bulk' }" |
| 카피·라벨 | "[저장] / [저장 안 함] / [취소]" |
| 가드·권한 분기 | "권한 없을 때 disabled 표기 / 컨트롤 자체 비노출" |

### Spec 모호성 식별 절차

1. Concept 책임·미정 섹션을 훑어 **"X 가 가능하다 / 사용한다 / 다룬다"** 류 약속 추출
2. 각 약속에 대해 위 7 차원 점검 — 결정 필요 항목 식별
3. 결정 필요 항목 → 해당 ticket 본문의 §수용 기준 / §구현 가이드 / §미정 에 분배
4. ticket 본문에서 결정 불가한 항목 → AskUserQuestion 으로 닫는다 (추정 금지). 닫지 못한 항목 → §미정 으로 남기고 후속 cascade 안내

### 자가 점검 — layer 흐려짐 신호

- ticket 본문이 spec 약속을 그대로 옮겨 적기만 함 → 구체화 부족 (write 가 자의 결정 강요받음)
- spec/concept 본문에 7 차원 결정이 들어가 있음 → spec cascade. plan / add-concept 으로 돌려 모호화 후 ticket 으로 이관

## 공통 티켓 출력 형식

```markdown
## 목표
[Concept에서 도출]

## 관련 Concept
- [~/Projects/flex/til/spec/{feature}/concepts/{name}.md] — [설명]

## 수용 기준
- [ ] [기준]

## 구현 가이드
- [파일 경로, 함수명, 구현 방향]

## 코드 위치
- `path/to/file.tsx` — [역할]

## 참고
- **피그마**/**노션**/**관련 티켓**: [link]
```

---

## 생성 모드

### 1. 스펙 로드

`~/Projects/flex/til/spec/{feature}/{FEATURE}.md` + `concepts/*.md`. 없으면 `/drill:plan` 안내.

### 2. Linear 프로젝트 설정

`list_teams` → 팀 선택. 선택적으로 `list_projects`, `list_issue_labels`, `list_issue_statuses` 캐싱.

### 3. 티켓 분해 계획

**원칙**: Concept ↔ 티켓 **N:N** · 한 티켓 ≤ 8시간 · 수용 기준은 Concept 책임·에지에서 도출. **Spec 모호성 식별 절차를 분해 중 적용** (§Layer 경계).

**FE 3방향 분해**: [플로우] 기준 쪼개기 + [마크업]·[API] 작업량에 따라 N:N.

| 방향 | prefix | 담는 내용 |
|------|--------|----------|
| UX 플로우 | `[플로우]` | 상태 전이·화면 전환·권한 분기·빈/에러·뷰 모델·미정 |
| UI 마크업 | `[마크업]` | 레이아웃·컴포넌트·variant·스타일 |
| API 연동 | `[API]` | 엔드포인트·요청/응답 타입·로딩/에러·폴링/구독 |

**분해 규칙**:
- 플로우는 작업량 무관 작은 단위로. 여러 UX 시나리오 섞이면 플로우부터 쪼갬
- 작업량 많은 쪽 N (플로우 1 → 마크업/API N)
- **공유 API/컴포넌트**: 여러 플로우 → 마크업·API 1로 머지
- 제목은 동일 본문에 prefix만 다르게 — 예: `[플로우]/[마크업]/[API] 외부 서비스 지식 LNB`
- 디자인 미정이어도 플로우 선행 가능, 마크업은 임의 시작 후 디자인 확정 시 재작업
- **뷰 모델은 별도 티켓 아님** — 플로우 안에서 자연스럽게 정의

**Concept ↔ 플로우는 1:1 아님**. 각 플로우 티켓은 관련 Concept 경로를 "참고" 에 나열.

**의존 관계**:
- [마크업]/[API] → 대응 [플로우] `blockedBy` 또는 `relatedTo`
- 공유 [마크업]·[API] 는 페어(공통) 표기 + 모든 공유 플로우 relatedTo
- BE 선행 필요 [API] 는 BE 티켓 `blockedBy`

**마크업 추상화**: 여러 플로우의 유사 UI 패턴(리스트·배지·모달 등) 은 공통 티켓 후보 식별. **AI 독단 금지** — 확정은 Phase 3.5.

**분해 테이블 예시**:
```
| # | 기능 | 플로우 | 마크업 | API | 관련 Concept |
| 1 | LNB + 랜딩 | [플로우] | [마크업] | [API] | integration, navigation |
| 2 | 연결 플로우 | [플로우] | [마크업] | [API] | integration, setting |
```

부모/하위 구조는 필수 아님 — AskUserQuestion으로 확인.

### 3.5 공통 마크업 확정

분해 테이블 초안 완성 후 마크업 열에서 유사 UI 패턴 후보 → AskUserQuestion(다중 선택) 으로 일괄 확인. 확정된 공통은 `(공통)` 표기 신규 행 추가. 확정 전 Phase 4 진행 금지. Phase 5는 3.5 결과만 그대로 따름 (추가 질문 없음).

### 4. 코드 탐색 + 구현 가이드

`Task` 로 `drill-code-explore` agent 1회 호출 (A 모드):
- 입력: `feature_name`, `concepts`, `ticket_titles` (Phase 3.5 결과), hints
- 출력: 티켓별 `related_files` + 파일 역할·심볼

리포트의 **Ticket Mapping** + **Files** 를 각 티켓의 §코드 위치 / §구현 가이드 로. 추가 Read 는 수정 위치 확인이 꼭 필요할 때만 (1~2 파일).

`uncertain: true` 티켓은 코드 위치 "미정" + Phase 6 안내에 포함.

### 5. Linear 티켓 생성

- **[플로우] 먼저** 생성 (작은 완결 단위 UX 1개당 1개)
- 각 플로우에 [마크업]/[API] (1:1:1 강제 없음, N:N)
- 공유 마크업은 Phase 3.5 확정만 `(공통)` 로 머지
- [마크업]/[API] → [플로우] `blockedBy`/`relatedTo`
- parentId 연결 또는 에픽 하위 플랫

**티켓별 description** — 공통: 관련 Concept · 수용 기준 · 구현 가이드 · 코드 위치 + **§Layer 경계 7 차원 적용된 구체 결정**.

> **수용 기준 = 구체 결정**: spec/concept 약속을 그대로 옮기지 말고, write 단계 자의 결정이 필요 없도록 7 차원이 닫혀있어야 함. 닫지 못한 항목은 §미정 + AskUserQuestion 으로 처리한 사용자 결정만 기록.

### 6. 안내

Spec 파일에 Linear 섹션 추가 안 함. 생성된 티켓 목록+URL만 안내.

---

## 강화 모드

### 1. 티켓 로드·분석

`get_issue` + `list_comments` → 기존 정보 분석 (증상·재현·Figma·기대 동작·코드 위치·수용 기준) → 갭 목록.

### 2. Spec/Concept 연결

티켓에서 feature name 추출 → `~/Projects/flex/til/spec/` Glob → 있으면 로드, 없으면 Phase 3.

### 3. 자동 컨텍스트 수집

- Figma URL: `get_design_context` + `get_screenshot`
- 코드베이스: `Task` 로 `drill-code-explore` B 모드 — 티켓 제목·증상·재현 경로를 `search_intent`, 도메인 명사를 `hints`. 반환된 top_candidates 만 필요 시 Read

### 4. 갭 인터뷰

빠진 항목 한국어 AskUserQuestion. 우선순위: 재현 경로 · 기대 동작 · 영향 범위 · 코드 위치 · 특수 조건 · 원인 추정(선택) · 수용 기준 · **§Layer 경계 7 차원 (how 차원)**.

소크라테스식 파고들기는 `plan` skill `§2` 참고 (정의·가정·근거·함의·반례 + Follow-up 강제). **질문 차원 = how 만** — plan 에서 닫힌 what/why 의문 시 plan 으로 cascade.

### 5. 티켓 업데이트

기존 description 보존. 하단에 구조화 섹션 추가 (관련 Concept / 구현 가이드 / 코드 위치 / 수용 기준). 사용자 확인 후 `save_issue({ id, description })`.

---

## 사용 도구

| 도구 | 용도 |
|------|------|
| `get_issue` / `list_teams` / `list_projects` / `list_issue_labels` / `list_issue_statuses` / `save_issue` / `list_comments` | Linear |
| `get_design_context` / `get_screenshot` | Figma |
| `Task(drill-code-explore)` | 코드 탐색 |
| Glob/Grep/Read | 수정 위치 확인 보조 |

## 제약

- 코드 수정 금지 (Linear 티켓만)
- 한국어, 티켓 생성/수정 전 사용자 확인
- Concept 경로: `~/Projects/flex/til/spec/{feature}/concepts/{name}.md`
- 각 티켓 ≤ 8시간

## 에러

- Linear API 실패 → 에러 + 수동 복사 텍스트 제공
- 스펙 없음 → `/drill:plan` 안내
- Figma 조회 실패 → 인터뷰에서 직접 수집
- 코드 탐색 결과 없음 → 코드 위치 AskUserQuestion
