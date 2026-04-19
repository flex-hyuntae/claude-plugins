---
name: prepare
description: Spec/Concepts를 기반으로 Linear 티켓을 생성하거나 기존 티켓을 강화합니다
disable-model-invocation: true
argument-hint: "[spec-feature-name|linear-issue-url|issue-id]"
---

# Prepare

Spec/Concepts를 기반으로 Linear 티켓을 생성하거나, 기존 티켓을 Spec 기반으로 강화합니다.
인자에 따라 자동으로 모드를 판단합니다.

## 모드 판단

| 인자 | 모드 | 동작 |
|------|------|------|
| feature name (예: `job-grade-modal`) | **생성** | spec/ 로드 → 티켓 분해 → Linear 생성 |
| Linear URL/ID (예: `CORE-1234`) | **강화** | 기존 티켓 로드 → spec 연결 → 강화 |
| 인자 없음 | 질문 | AskUserQuestion으로 모드 확인 |

## 공통: 티켓 출력 형식

생성/강화 모두 동일한 형식으로 티켓을 작성합니다:

```markdown
## 목표
[Concept에서 도출된 목표]

## 관련 Concept
- [~/Projects/flex/til/spec/{feature}/concepts/{name}.md] — [설명]

## 수용 기준
- [ ] [기준 1]
- [ ] [기준 2]

## 구현 가이드
- [파일 경로, 함수명, 구체적 구현 방향]

## 코드 위치
- `path/to/file.tsx` — [역할]

## 참고
- **피그마**: [link]
- **노션**: [link]
- **관련 티켓**: [link]
```

---

## 생성 모드 (Create)

### Phase 1: 스펙 문서 로드

- `~/Projects/flex/til/spec/{feature-name}/{FEATURE-NAME}.md` 읽기
- `~/Projects/flex/til/spec/{feature-name}/concepts/*.md` 파일들 모두 읽기
- 디렉토리가 없으면: `/drill:plan`을 먼저 실행하세요

### Phase 2: Linear 프로젝트 설정

1. **팀 선택**: `mcp__linear-server__list_teams` → 사용자에게 팀 선택 요청
2. **프로젝트 선택** (선택적): `mcp__linear-server__list_projects` → 연결할 프로젝트 선택
3. **라벨 목록**: `mcp__linear-server__list_issue_labels` → 사용 가능한 라벨 캐싱
4. **상태값 목록**: `mcp__linear-server__list_issue_statuses` → 사용 가능한 상태값 캐싱

### Phase 3: 티켓 분해 계획

Concept들을 분석하여 티켓 분해안을 작성합니다.

**분해 기준:**
- Concept과 티켓은 N:N 관계
- 하나의 티켓은 최대 8시간 이내 완료 가능한 크기
- 각 티켓의 수용 기준은 관련 Concept의 책임·에지 케이스에서 도출

**FE 4방향 분해:**

FE 티켓은 하나의 기능 단위를 **네 방향으로 쪼개는 것**을 기본으로 합니다. 디자인·API가 비동기로 준비되는 현실에서 각 방향을 독립적으로 진행할 수 있게 하기 위함.

| 방향 | 제목 prefix | 담는 내용 |
|------|------------|----------|
| 모델 정의 | `[모델]` | 타입/인터페이스, 데이터 구조, 상태 모델, 도메인 스키마 |
| UX 플로우 | `[플로우]` | 상태 전이, 화면/모달 전환, 권한별 분기, 빈/에러 상태, 미정 항목 명시 |
| UI 마크업 | `[마크업]` | 레이아웃, 컴포넌트 구성, variant, 스타일링 |
| API 연동 | `[API]` | 엔드포인트 호출, 요청/응답 타입, 로딩/에러 처리, 필요 시 폴링/구독 |

**원칙:**

- **한 기능 단위 = 모델 1 + 플로우 1 + 마크업 1 + API 1** (네 쌍을 짝지어 생성)
- 제목은 동일 본문에 prefix만 다르게 — 예) `[모델]/[플로우]/[마크업]/[API] 외부 서비스 지식 LNB`
- **디자인이 아직 없어도 모델·플로우는 즉시 선행** 가능. 마크업은 임의 마크업으로 시작한 뒤 디자인 확정 시 재작업
- 모델이 단순(예: 단일 ID 파라미터)이고 공유 범위가 없으면 [모델] 대신 [API] 안에 흡수해도 됨 — 기본은 분리

**의존 관계 기본 패턴:**

- [플로우] / [마크업] / [API] 는 동일 기능의 [모델] 을 `blockedBy` 로 참조 (타입 공유가 있으므로)
- [마크업] / [API] 는 [플로우] 를 추가로 `blockedBy` 또는 `relatedTo` 로 참조
- BE 티켓이 선행되어야 하는 [API] 는 해당 BE 티켓을 `blockedBy` 로 함께 참조

**부가 축 (필요 시):**

- **i18n**: 다국어 처리 (마크업에 흡수 가능)
- **권한/Feature Flag**: 플로우 안에서 분기 명시

**분해 계획 테이블:**

```
| # | 기능 | 모델 | 플로우 | 마크업 | API | 관련 Concept |
|---|------|------|--------|--------|-----|-------------|
| 1 | LNB + 랜딩             | [모델] | [플로우] | [마크업] | [API] | integration, navigation |
| 2 | 연결 플로우             | [모델] | [플로우] | [마크업] | [API] | integration, setting |
| 3 | 서비스별 상세 페이지   | [모델] | [플로우] | [마크업] | [API] | integration, knowledge |
```

> 부모/하위 이슈 구조는 필수가 아닙니다. 플로우 티켓을 부모로 두고 마크업/API를 하위로 붙이거나, 모두 플랫하게 에픽 하위로 나열하거나 선택 가능. 사용자에게 확인합니다.

사용자 확인 후 수정 반영.

### Phase 4: 코드 탐색 및 구현 가이드 작성

각 티켓에 대해 코드베이스를 탐색하여 구현 가이드를 작성합니다.

- glob/grep으로 관련 파일 검색
- read로 핵심 파일 읽기
- 파일 경로, 수정할 위치, 구현 방향을 구체적으로 기술

### Phase 5: Linear 티켓 생성

**생성:**
- 분해 계획의 각 기능 단위마다 **[모델] / [플로우] / [마크업] / [API] 네 티켓을 쌍으로 생성**
- 제목은 동일 본문에 prefix만 다르게 (`[모델] …` / `[플로우] …` / `[마크업] …` / `[API] …`)
- [플로우] / [마크업] / [API] 는 [모델] 티켓을 `blockedBy` 로 참조, [마크업] / [API] 는 [플로우] 를 추가 참조
- 부모/하위 구조가 필요하면 parentId 연결, 아니면 에픽 하위 플랫

각 티켓 description에 포함:
- **[모델]**: 타입/인터페이스 정의, 데이터 구조, 공유 모델 파일 위치, 페어 플로우/마크업/API
- **[플로우]**: 상태 전이, 분기, 빈/에러 상태, 미정 항목, 관련 Concept, 페어 모델/마크업/API
- **[마크업]**: 컴포넌트 목록, variant, 디자인 링크 (없으면 "임의 마크업 선행" 명시), 페어 모델/플로우/API
- **[API]**: 엔드포인트 목록, 요청/응답 스펙, API 상태(기존 재사용 / 신규 / 미정), 페어 모델/플로우/마크업, BE 선행 티켓

공통:
- 관련 Concept 경로 (`~/Projects/flex/til/spec/{feature}/concepts/{name}.md`)
- 수용 기준 (Concept의 책임·에지 케이스에서 도출)
- 구현 가이드 / 코드 위치 (코드 탐색 결과)

### Phase 6: Spec 파일 업데이트

생성된 티켓 정보를 Spec 파일에 반영하지 않습니다 (Linear 섹션 없음).
대신 사용자에게 생성된 티켓 목록과 URL을 안내합니다.

---

## 강화 모드 (Enrich)

### Phase 1: 티켓 로드 및 분석

- Linear URL/ID에서 이슈 로드 (`mcp__linear-server__get_issue`)
- 코멘트 조회 (`mcp__linear-server__list_comments`)
- 기존 정보 분석 (증상, 재현 경로, 스크린샷, Figma, 기대 동작, 코드 위치, 수용 기준)
- 갭 목록 생성

### Phase 2: Spec/Concept 연결

- 티켓 내용에서 feature name 추출 시도
- `~/Projects/flex/til/spec/` 디렉토리에서 관련 스펙 검색 (Glob)
- 관련 Concept이 있으면 로드하여 티켓 강화에 활용
- 없으면 Phase 3로 진행

### Phase 3: 자동 컨텍스트 수집

**Figma 조회** (URL 발견 시):
```
mcp__figma__get_design_context({ fileKey, nodeId })
mcp__figma__get_screenshot({ fileKey, nodeId })
```

**코드베이스 탐색** (항상 실행):
- 티켓 키워드로 glob/grep 검색
- 핵심 파일 read

### Phase 4: 갭 인터뷰

Phase 1에서 빠진 항목만 질문합니다. AskUserQuestion 사용, 한국어.

**질문 우선순위** (이미 있는 정보는 건너뜀):
1. 재현 경로
2. 기대 동작
3. 영향 범위
4. 코드 위치 확인
5. 특수 조건
6. 원인 추정 (선택)
7. 수용 기준

### Phase 5: 티켓 업데이트

**기존 내용 보존:** 기존 티켓 description을 덮어쓰지 않습니다. 기존 내용 아래에 구조화된 정보를 추가하거나, 기존 섹션을 보강하는 방식으로 업데이트합니다.

```markdown
<!-- 기존 티켓 내용 그대로 유지 -->
{기존 description}

---
<!-- 아래부터 강화된 내용 -->
## 관련 Concept
- [~/Projects/flex/til/spec/{feature}/concepts/{name}.md] — [설명]

## 구현 가이드
- [파일 경로, 구현 방향]

## 코드 위치
- `path/to/file.tsx` — [역할]

## 수용 기준
- [ ] [기준]
```

사용자 확인 후 Linear 업데이트:
```
mcp__linear-server__save_issue({ id, description })
```

---

## 사용할 MCP 도구

| 도구 | 용도 |
|------|------|
| `mcp__linear-server__get_issue` | 티켓 상세 조회 |
| `mcp__linear-server__list_teams` | 팀 목록 조회 |
| `mcp__linear-server__list_projects` | 프로젝트 목록 조회 |
| `mcp__linear-server__list_issue_labels` | 라벨 목록 조회 |
| `mcp__linear-server__list_issue_statuses` | 상태값 목록 조회 |
| `mcp__linear-server__save_issue` | 이슈 생성/수정 |
| `mcp__figma__get_design_context` | Figma 디자인 분석 |
| `mcp__figma__get_screenshot` | Figma 스크린샷 |
| Glob / Grep / Read | 코드베이스 탐색 |

## 중요 사항

- **코드 수정 금지**: 이 스킬은 Linear 티켓만 생성/수정. 소스 코드 수정 안 함
- **언어**: 모든 커뮤니케이션은 한국어로 진행
- **Concept 경로**: 티켓 내 Concept 링크는 `~/Projects/flex/til/spec/{feature}/concepts/{name}.md` 형식
- **확인**: 티켓 생성/수정 전 반드시 사용자 확인
- **크기**: 각 티켓은 최대 8시간 이내 완료 가능한 크기

## 에러 처리

- Linear API 실패: 에러 메시지 표시, 수동 복사용 텍스트 제공
- 스펙 없음: `/drill:plan` 실행 안내
- Figma 조회 실패: 인터뷰에서 직접 수집
- 코드 탐색 결과 없음: 사용자에게 코드 위치 질문
