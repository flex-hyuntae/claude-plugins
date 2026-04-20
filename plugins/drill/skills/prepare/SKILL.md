---
name: prepare
description: Spec/Concepts를 기반으로 Linear 티켓을 생성하거나 기존 티켓을 강화합니다
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

**원칙**: Concept ↔ 티켓 **N:N** · 한 티켓 ≤ 8시간 · 수용 기준은 Concept 책임·에지에서 도출.

**FE 3방향 분해**: [플로우] 기준으로 쪼개고 [마크업]·[API]는 작업량에 따라 N:N.

| 방향 | prefix | 담는 내용 |
|------|--------|----------|
| UX 플로우 | `[플로우]` | 상태 전이·화면/모달 전환·권한 분기·빈/에러 상태·**뷰 모델**(화면 상태 shape / derived / UI enum)·미정 명시 |
| UI 마크업 | `[마크업]` | 레이아웃·컴포넌트 구성·variant·스타일 |
| API 연동 | `[API]` | 엔드포인트·요청/응답 타입·로딩/에러·필요 시 폴링·구독 |

**분해 규칙**:
- **플로우 기준**: 작업량과 무관하게 명확히 작은 단위로. 여러 UX 시나리오 섞이면 플로우부터 쪼갬
- 작업량 많은 쪽 N (플로우 1 → 마크업 N, 플로우 1 → API N)
- **공유 API/컴포넌트**: 여러 플로우 → 마크업·API 1로 머지
- 제목은 동일 본문에 prefix만 다르게 — 예: `[플로우]/[마크업]/[API] 외부 서비스 지식 LNB`
- 디자인 미정이어도 플로우는 선행 가능, 마크업은 임의로 시작 후 디자인 확정 시 재작업
- **뷰 모델은 별도 티켓 아님** — 플로우 안에서 자연스럽게 정의, 연관 플로우끼리 relatedTo

**Concept ↔ 플로우**: 1:1 아님. Concept 하나가 여러 플로우에 걸치거나, Concept 하위에 여러 플로우 가능. 플로우 = 작은 완결 단위 UX 시나리오. 각 플로우 티켓은 관련 Concept 경로를 "참고"에 나열만.

**의존 관계**:
- [마크업]/[API] → 대응 [플로우] 를 `blockedBy` 또는 `relatedTo`
- 공유 [마크업]·[API] 는 페어(공통) 표기 + 모든 공유 플로우 relatedTo
- BE 선행 필요 [API] 는 BE 티켓 `blockedBy`
- 연관 플로우끼리 `relatedTo`

**마크업 추상화**: 여러 플로우의 유사 UI 패턴(리스트·배지·모달 등)은 공통 티켓으로. **AI 독단 금지** — AskUserQuestion으로 확인 후 공통 분리. 공통 확정 시 `[마크업] ... (공통)` 신규 생성, 각 페이지는 "공통 컴포넌트 사용" + 고유 요소만.

**부가 축**: i18n(마크업 흡수 가능) · 권한/Feature Flag(플로우 내 분기).

**분해 테이블 예시**:

```
| # | 기능 | 플로우 | 마크업 | API | 관련 Concept |
|---|------|--------|--------|-----|-------------|
| 1 | LNB + 랜딩 | [플로우] | [마크업] | [API] | integration, navigation |
| 2 | 연결 플로우 | [플로우] | [마크업] | [API] | integration, setting |
```

부모/하위 구조는 필수 아님 — AskUserQuestion으로 확인.

### 4. 코드 탐색 + 구현 가이드

각 티켓마다 glob/grep → 핵심 파일 read → 파일 경로·수정 위치·구현 방향 구체 기술.

### 5. Linear 티켓 생성

- **[플로우] 먼저** 생성 (작은 완결 단위 UX 시나리오 1개당 1개)
- 각 플로우에 [마크업]/[API] 생성 — **1:1:1 강제 없음**, 작업량 따라 N:N, 공유 시 "공통" 머지
- 마크업 공유는 AskUserQuestion 확인 후 분리
- 제목 prefix만 다르게, 공통은 "(공통)" 표기
- [마크업]/[API] → [플로우] `blockedBy`/`relatedTo`
- parentId 연결 또는 에픽 하위 플랫

**티켓별 description**:
- [플로우]: 상태 전이·분기·빈/에러·뷰 모델·미정·관련 Concept·페어 마크업/API·연관 플로우
- [마크업]: 컴포넌트·variant·디자인 링크(없으면 "임의 마크업 선행")·페어 플로우/API
- [API]: 엔드포인트·요청/응답·API 상태(재사용/신규/미정)·페어 플로우/마크업·BE 선행

공통: 관련 Concept 경로 · 수용 기준 · 구현 가이드·코드 위치.

### 6. 안내

Spec 파일에 Linear 섹션 추가 안 함. 생성된 티켓 목록+URL만 안내.

---

## 강화 모드

### 1. 티켓 로드·분석

`get_issue` + `list_comments` → 기존 정보 분석(증상·재현·Figma·기대 동작·코드 위치·수용 기준) → 갭 목록.

### 2. Spec/Concept 연결

티켓에서 feature name 추출 → `~/Projects/flex/til/spec/` Glob → 있으면 로드, 없으면 Phase 3.

### 3. 자동 컨텍스트 수집

- Figma URL 발견 시: `get_design_context` + `get_screenshot`
- 코드베이스 탐색 (항상): glob/grep → 핵심 파일 read

### 4. 갭 인터뷰

빠진 항목만 질문 (한국어 AskUserQuestion). 우선순위: 재현 경로 · 기대 동작 · 영향 범위 · 코드 위치 · 특수 조건 · 원인 추정(선택) · 수용 기준.

### 5. 티켓 업데이트

**기존 description 보존**. 하단에 구조화된 섹션 추가 (관련 Concept / 구현 가이드 / 코드 위치 / 수용 기준). 사용자 확인 후 `save_issue({ id, description })`.

---

## 사용 도구

| 도구 | 용도 |
|------|------|
| `get_issue`, `list_teams`, `list_projects`, `list_issue_labels`, `list_issue_statuses`, `save_issue`, `list_comments` | Linear |
| `get_design_context`, `get_screenshot` | Figma |
| Glob/Grep/Read | 코드 탐색 |

## 제약

- 코드 수정 금지 (Linear 티켓만)
- 한국어, 티켓 생성/수정 전 사용자 확인
- Concept 경로: `~/Projects/flex/til/spec/{feature}/concepts/{name}.md`
- 각 티켓 ≤ 8시간

## 에러

- Linear API 실패 → 에러 메시지 + 수동 복사 텍스트 제공
- 스펙 없음 → `/drill:plan` 안내
- Figma 조회 실패 → 인터뷰에서 직접 수집
- 코드 탐색 결과 없음 → 코드 위치 AskUserQuestion
