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

- `~/Projects/flex/til/spec/{feature-name}/SPEC.md` 읽기
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
- 각 티켓의 수용 기준은 관련 Concept의 SHOULD 항목에서 도출

**FE 작업 플로우 기반 분해:**

티켓은 아래 플로우 단위로 먼저 나누고, 각 플로우 내에서 더 상세하게 분해합니다:

| 순서 | 플로우 | 설명 |
|------|--------|------|
| 1 | 모델 정의 | 타입, 인터페이스, 데이터 구조 |
| 2 | UI 생성 | 컴포넌트, 레이아웃, 스타일링 |
| 3 | UX 플로우 | 상태 관리, 인터랙션, 네비게이션 |
| 4 | API 연동 | API 호출, 데이터 페칭, 에러/로딩 처리 |

필요 시 추가 플로우:
- **i18n**: 다국어 처리
- **권한/Feature Flag**: 조건부 접근, flag 기반 분기

**분해 계획 테이블:**

```
| # | 플로우 | 제목 | 관련 Concept | 예상 크기 |
|---|--------|------|-------------|-----------|
| 1 | 모델 정의 | [작업명] | table, search | S |
| 2 | UI 생성 | [작업명] | table | M |
| 3 | UX 플로우 | [작업명] | table, error-panel | M |
| 4 | API 연동 | [작업명] | search | S |
```

> 부모/하위 이슈 구조는 필수가 아닙니다. 플랫하게 생성하거나, 필요 시 부모 이슈로 묶을 수 있습니다. 사용자에게 확인합니다.

사용자 확인 후 수정 반영.

### Phase 4: 코드 탐색 및 구현 가이드 작성

각 티켓에 대해 코드베이스를 탐색하여 구현 가이드를 작성합니다.

- glob/grep으로 관련 파일 검색
- read로 핵심 파일 읽기
- 파일 경로, 수정할 위치, 구현 방향을 구체적으로 기술

### Phase 5: Linear 티켓 생성

**생성:**
- 분해 계획 순서대로 이슈 생성 (`mcp__linear-server__save_issue`)
- 부모/하위 구조가 필요하면 parentId 연결, 아니면 플랫하게 생성

각 티켓 description에 포함:
- 목표 (Concept에서 도출)
- 관련 Concept 경로 (`~/Projects/flex/til/spec/{feature}/concepts/{name}.md`)
- 수용 기준 (Concept의 SHOULD에서 도출)
- 구현 가이드 (코드 탐색 결과)
- 코드 위치

### Phase 6: SPEC.md 업데이트

생성된 티켓 정보를 SPEC.md에 반영하지 않습니다 (Linear 섹션 없음).
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
