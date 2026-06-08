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

## Layer 경계 — Spec 모호성(what/why) → Ticket 구체화(how) → Write(작성만)

prepare 의 핵심 책임은 **spec/concept 의 의도된 모호성(what/why) 을 ticket 본문에서 구체화(how)** 하는 것. 단계별 질문 차원·원칙은 `plan` skill `§Layer 경계` 참고. **본 단계 = how 차원**, plan 에서 닫힌 what/why 는 재논의하지 않는다 (의문 시 plan 으로 cascade).

> **티켓 = 구현 설계서**. 보통 write 시점에 plan 모드로 세울 구현 계획을 **prepare 가 선행해 ticket 본문에 박아두는 것이 기본 기대** — write 는 rules 기반 **작성에 집중**하고, 목표는 **"이 티켓대로 구현하면 누가 작성해도 동일한 결과"**. 단 write 에서 코드 탐색·설계 재고가 필요해질 수 있으며(티켓이 부족할 때), 이는 금지가 아니라 **모호성을 코드로 흡수하지 말고 prepare 로 돌아가 티켓을 강화하라는 신호**다.

### Ticket 본문이 닫아야 할 how 차원 — 2 층

spec 의 "X 가능" 약속을 충족하는 구체 결정. 본질은 **"이 약속을 구현하려면 어떤 결정이 필요한가?"**(제품 how) + **"그 결정을 코드로 어떻게 옮기는가?"**(구현 how).

**① 제품 how** — 무엇을 만드는가:

| 카테고리 | 결정 예시 |
|---------|----------|
| UI 구체화 (위치·매체·옵션·중복) | "AI 게시 셀 = Dropdown / OFF 시각 표식 = 제목 영역" / "Footer paginator 의 size selector·navigator·count 중 본 사이클 = navigator" / "다운로드: Callout + More 둘 다 vs 하나만" |
| 카탈로그 항목 | "Dropdown 항목 = ON / OFF" / "More 메뉴 = AI 게시·그룹 옮기기·삭제" |
| 시그니처·카피·가드 | "props discriminated union { variant: 'single' \| 'bulk' }" / "[저장] / [저장 안 함] / [취소]" / "권한 없을 때 disabled vs 비노출" |

**② 구현 how** — 코드로 어떻게 만드는가 (write 가 추가 설계 없이 따라 칠 수준):

| 카테고리 | 결정 예시 |
|---------|----------|
| 변경 파일 (신규/수정) | "`GradeModal.tsx` 신규 / `GradeList.tsx` 수정 — 행 클릭 핸들러 추가" |
| 함수·타입 시그니처 | "`useGradeForm(initial?: Grade): {...}` 추가" / "`type GradeFormState = {...}` 확장" |
| 따라야 할 기존 패턴 | "`SalaryModal.tsx:30` open/close 패턴 그대로 — react-hook-form + Dialog" |
| 재사용 vs 신규 | "목록 조회는 기존 `useGradeListQuery` 재사용 / 폼 스키마는 신규 `gradeSchema`" |
| 레이어 배치 | "검증 = `schema/grade.ts`, 화면 상태 = 컴포넌트 로컬, 서버 상태 = query" |

### Spec 모호성 식별 절차

1. Concept 책임·미정 섹션을 훑어 **"X 가 가능하다 / 사용한다 / 다룬다"** 류 약속 추출
2. 각 약속에 대해 **"이 약속을 구현하려면 어떤 결정이 필요한가?"**(제품 how) → **"그 결정을 코드로 옮기려면 무엇이 정해져야 하는가?"**(구현 how) 순서로 질문
3. 결정 필요 항목 → 해당 ticket 본문의 §수용 기준 / §구현 설계 / §미정 에 분배
4. ticket 본문에서 결정 불가한 항목 → AskUserQuestion 으로 닫는다 (추정 금지). 닫지 못한 항목 → §미정 으로 남기고 후속 cascade 안내

### 자가 점검 — layer 흐려짐 신호

- ticket 본문이 spec 약속을 그대로 옮겨 적기만 함 → 구체화 부족 (write 가 자의 결정 강요받음)
- 제품 how 만 있고 구현 how(변경 파일·시그니처·기존 패턴) 가 비어 있음 → write 가 코드 설계를 떠안음. 코드 탐색(Phase 4) 으로 채운다
- spec/concept 본문에 how 결정(위치·카탈로그·시그니처 등) 이 들어가 있음 → spec cascade. plan / add-concept 으로 돌려 모호화 후 ticket 으로 이관

## 공통 티켓 출력 형식

```markdown
## 목표
[Concept에서 도출]

## 관련 Concept
- [~/Projects/flex/til/spec/{feature}/concepts/{name}.md] — [설명]

## 수용 기준
- [ ] [검증 가능한 완료 조건]

## 구현 설계
<!-- write 가 추가 탐색·설계 없이 그대로 구현할 수준. 누가 구현해도 동일 결과가 목표. -->

### 변경 파일
- `path/to/file.tsx` (수정) — [역할] · [무엇을 어떻게 바꾸는지]
- `path/to/new.tsx` (신규) — [역할]

### 시그니처·타입
- `함수명(args): 반환타입` (추가/수정) — [용도]
- `type X = { ... }` (추가/확장)

### 따라야 할 기존 패턴
- `ref/file.tsx:42 심볼명` — [이 패턴을 따른다]
  ```ts
  // 따라 쓸 핵심만 ≤10줄
  ```

### 재사용 vs 신규
- [기존 util/hook/컴포넌트 재사용 vs 신규 — 결정 + 이유]

### 변경 명세
- [수용 기준별: 어느 파일 어느 심볼을 어떻게 — write 가 옮길 수 있게 서술]

### 의존
- `blockedBy {ID}` — [이 티켓이 쓰는 산출물(util·타입·컴포넌트)을 그 티켓이 신규 생성]
- `relatedTo {ID}` — [같은 파일·심볼 수정으로 충돌 가능 / 공유 산출물]

## 미정
- [AskUserQuestion 으로도 못 닫은 항목 — 후속 cascade / 다음 사이클 결정. 숨은 추정 대신 여기 명시]

## 참고
- **피그마**/**노션**/**관련 티켓**: [link]
```

> §구현 설계 = 이 ticket 의 핵심. 코드는 **포인터(`file:line 심볼`) 우선**, 따라 써야 할 핵심 패턴만 ≤10줄 인용 (본문 통째 복사 금지). 빈 하위 섹션은 생략.

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
- **코드 레벨 구현 의존**(산출물 공유·선행)은 Phase 4 정독에서 추가 식별 → §의존 + Phase 5 설정

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

### 4. 코드 탐색 → 구현 설계 작성

**2 단계: agent 가 후보를 좁히고, 메인 세션이 핵심 파일을 정독해 설계를 쓴다.** (agent 는 AskUserQuestion 불가·distill 만 반환하므로, 모호함을 물으려면 메인이 코드를 들고 있어야 한다.)

**4-a. 후보 좁히기** — `Task` 로 `drill-code-explore` agent 1회 호출 (A 모드):
- 입력: `feature_name`, `concepts`, `ticket_titles` (Phase 3.5 결과), hints
- 출력: 티켓별 `related_files` + 파일 역할·심볼 (distill — 본문 없음)

**4-b. 핵심 파일 정독** — 메인 세션이 직접 Read:
- `related_files` 중 각 티켓이 **실제로 수정/참조할 파일**을 정독 (티켓당 보통 2~5개, 필요하면 더). 본 단계는 코드 본문을 읽어야 설계가 가능하므로 "Read 최소화" 제약을 적용하지 않는다
- 정독하며 §구현 설계 칸(변경 파일 / 시그니처·타입 / 따라야 할 기존 패턴 / 재사용 vs 신규 / 변경 명세 / 의존) 을 채운다
- **구현 의존 식별**: 한 티켓의 신규 산출물(util·타입·컴포넌트)을 다른 티켓이 쓰면 → 후자 `blockedBy` 전자. 같은 파일·심볼을 여러 티켓이 수정하면 → `relatedTo`(충돌 주의). §의존에 이유와 함께 기록 → Phase 5 에서 Linear 필드로 설정 (ship 의 stacked PR 순서가 이 의존 그래프를 따른다)

**4-c. 코드 레벨 모호함 → 즉시 질문 (추정 금지)** — 정독 중 결정이 갈리는 지점이 드러나면 그 자리서 AskUserQuestion (메인이 코드를 들고 있으므로 즉시 가능):
- 같은 일을 하는 기존 패턴이 둘 이상 — 어느 것을 따를지
- 재사용 가능한 util/hook 이 있는지 불확실, 또는 재사용 vs 신규가 갈림
- 타입을 신규로 만들지 기존을 확장할지
- 로직을 어느 레이어(hook / util / component / query / store) 에 둘지
- 네이밍이 기존 컨벤션과 충돌

소크라테스식 파고들기는 `plan` skill `§2` 참고 (R.W. Paul 6 유형 + Follow-up 강제). **질문 차원 = 구현 how 만**. 닫은 결정은 §구현 설계에, 못 닫은 항목은 §미정에 명시.

`uncertain: true` 또는 정독으로도 설계 불가한 티켓 → §구현 설계 "미정" + Phase 6 안내에 포함.

### 4.5 재현성 게이트 (티켓 생성 전 필수)

각 티켓이 **"누가 구현해도 동일 결과"** 수준인지 점검. 통과 못 하면 Phase 4 로 돌아가 정독/질문.

**1) 체크리스트** — 티켓마다 자문, 미충족 항목은 §4-c 질문 또는 §미정:
- [ ] 변경 파일이 신규/수정 표시와 함께 특정됐다
- [ ] 추가/수정할 함수·타입 시그니처가 적혔다
- [ ] 따라야 할 기존 패턴이 포인터(`file:line`)로 가리켜졌다
- [ ] 재사용 vs 신규가 이유와 함께 결정됐다
- [ ] 각 수용 기준이 변경 명세의 어느 항목으로 충족되는지 추적된다
- [ ] 다른 티켓 산출물에 대한 구현 의존이 §의존 + `blockedBy`/`relatedTo` 로 설정됐다
- [ ] 남은 모호함이 §미정 에 명시됐다 (숨은 추정 없음)

**2) 점수 게이트** — 구현 설계 차원에 `0 / 25 / 50 / 75 / 100` 점:

| 차원 | 0점 | 100점 |
|------|-----|-------|
| 파일 특정 | 어느 파일인지 모름 | 변경 파일 전부 신규/수정과 함께 특정 |
| 시그니처 확정 | 함수·타입 형태 불명 | 추가/수정 시그니처 확정 |
| 기존 패턴 연결 | 맨바닥부터 추정 | 따라야 할 기존 코드 포인터 명시 |
| 변경 명세 | "알아서 구현" | 수용 기준별 변경 위치·방식 서술 |
| 모호함 해소 | 추정으로 덮음 | 갈리는 지점 질문 완료 또는 §미정 명시 |

**게이트**: 각 차원 ≥ 75점 AND 평균 모호성 ≤ 15%. 미달 차원부터 Phase 4 재정독/질문. **자가 평가 금지** — 0/100 정의를 인용해 보수적으로(낮게) 매긴다 (plan `§2` 철학과 동일).

### 5. Linear 티켓 생성

Phase 4.5 게이트 통과한 티켓만 생성.

- **[플로우] 먼저** 생성 (작은 완결 단위 UX 1개당 1개)
- 각 플로우에 [마크업]/[API] (1:1:1 강제 없음, N:N)
- 공유 마크업은 Phase 3.5 확정만 `(공통)` 로 머지
- [마크업]/[API] → [플로우] `blockedBy`/`relatedTo` (분해 의존)
- **구현 의존** (Phase 4 식별): 산출물 공유·선행 코드 → `blockedBy` / 같은 심볼 수정 → `relatedTo`. §의존에 적은 이유와 함께 설정 (ship 이 이 그래프로 stacked PR 순서 결정)
- parentId 연결 또는 에픽 하위 플랫

**티켓별 description** — §공통 티켓 출력 형식: 관련 Concept · 수용 기준 · **§구현 설계**(변경 파일·시그니처·기존 패턴·재사용·변경 명세) · 참고.

> **수용 기준 = 구체 결정 + 구현 설계 = 재현 가능**: spec/concept 약속을 그대로 옮기지 말고, 제품 how(UI 구체화 / 카탈로그 / 시그니처·카피·가드) 와 구현 how(변경 파일 / 시그니처 / 기존 패턴 / 재사용 / 변경 명세) 를 둘 다 닫는다. 닫지 못한 항목은 §미정 + AskUserQuestion 으로 처리한 사용자 결정만 기록 — write 가 자의 결정·코드 탐색을 떠안지 않게.

### 6. 안내

Spec 파일에 Linear 섹션 추가 안 함. 생성된 티켓 목록+URL만 안내.

---

## 강화 모드

### 1. 티켓 로드·분석

`get_issue` + `list_comments` → 기존 정보 분석 (증상·재현·Figma·기대 동작·구현 설계·수용 기준) → 갭 목록.

### 2. Spec/Concept 연결

티켓에서 feature name 추출 → `~/Projects/flex/til/spec/` Glob → 있으면 로드, 없으면 Phase 3.

### 3. 자동 컨텍스트 수집

- Figma URL: `get_design_context` + `get_screenshot`
- 코드베이스: `Task` 로 `drill-code-explore` B 모드 — 티켓 제목·증상·재현 경로를 `search_intent`, 도메인 명사를 `hints`. 반환된 top_candidates 중 **실제 수정/참조할 핵심 파일은 메인 세션이 정독** (구현 설계를 채워야 하므로 Read 최소화 적용 안 함)

### 4. 갭 인터뷰

빠진 항목 한국어 AskUserQuestion. 우선순위: 재현 경로 · 기대 동작 · 영향 범위 · 수용 기준 · **제품 how**(UI 구체화·카탈로그·시그니처·카피·가드) · **구현 how**(변경 파일·시그니처·기존 패턴·재사용·레이어 — §생성 모드 4-c 모호함 트리거와 동일) · 특수 조건 · 원인 추정(선택).

소크라테스식 파고들기는 `plan` skill `§2` 참고 (R.W. Paul 6 유형 — ① 정의 / ② 가정 점검 / ③ 근거 / ④ 다른 관점 / ⑤ 함의 / ⑥ 메타 + Follow-up 강제). **질문 차원 = how 만** (제품·구현 how) — plan 에서 닫힌 what/why 의문 시 plan 으로 cascade.

강화 결과도 §생성 모드 4.5 재현성 게이트로 점검 후 `save_issue`.

### 5. 티켓 업데이트

기존 description 보존. 하단에 구조화 섹션 추가 (관련 Concept / 수용 기준 / §구현 설계). Phase 4.5 게이트 통과 확인 후 `save_issue({ id, description })`.

---

## 사용 도구

| 도구 | 용도 |
|------|------|
| `get_issue` / `list_teams` / `list_projects` / `list_issue_labels` / `list_issue_statuses` / `save_issue` / `list_comments` | Linear |
| `get_design_context` / `get_screenshot` | Figma |
| `Task(drill-code-explore)` | 코드 후보 좁히기 (distill, Phase 4-a) |
| Read | 핵심 파일 정독 — 구현 설계 작성 (Phase 4-b) |
| Glob/Grep | 추가 위치 확인 보조 |

## 제약

- 코드 수정 금지 (Linear 티켓만) — 단 **핵심 파일 정독(Read)은 구현 설계를 위해 적극 수행**
- 한국어, 티켓 생성/수정 전 사용자 확인
- **코드 레벨 모호함은 추정 금지** — 메인이 코드를 들고 있을 때 그 자리서 AskUserQuestion (§4-c)
- 티켓 = 구현 설계서 — write 가 작성에 집중하도록 채운다 (write 탐색·설계가 불가피해지면 prepare 강화로 환류되는 게 정상 흐름)
- Concept 경로: `~/Projects/flex/til/spec/{feature}/concepts/{name}.md`
- 각 티켓 ≤ 8시간

## 에러

- Linear API 실패 → 에러 + 수동 복사 텍스트 제공
- 스펙 없음 → `/drill:plan` 안내
- Figma 조회 실패 → 인터뷰에서 직접 수집
- 코드 탐색 결과 없음 → 구현 설계 항목 AskUserQuestion (추정 금지)
