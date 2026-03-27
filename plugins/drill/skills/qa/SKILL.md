---
name: qa
description: Spec, Concepts, Decision Log, 구현 코드를 기반으로 QA 테스트 케이스를 작성합니다
disable-model-invocation: true
argument-hint: "[spec-feature-name]"
---

# QA

Spec + Concepts + Decision Log + 구현 코드를 종합하여 체계적인 QA 테스트 케이스를 작성합니다.
Concept의 SHOULD 항목을 기반으로 커버리지 매트릭스를 구성하여 누락 없이 TC를 작성합니다.

## Workflow

### Phase 1: 소스 수집

사용자에게 아래 정보를 수집합니다.

**필수 입력:**
1. **Feature name**: spec 디렉토리명 (예: `job-grade-modal`)
   - 인자로 주어지면 자동 사용
   - 없으면 `~/Projects/flex/til/spec/` 하위 디렉토리 목록에서 선택

**선택 입력:**
3. **Figma 디자인 URL**: UI/UX TC 보강용
4. **Feature flag**: 테스트에 필요한 flag
5. **추가 Linear 프로젝트 ID**: spec에 없는 추가 맥락

### Phase 2: 소스 분석

수집한 소스를 **병렬로** 분석합니다.

#### 2-1. Spec/Concept/Decision 분석

- `~/Projects/flex/til/spec/{feature}/{FEATURE-NAME}.md` 읽기
- `~/Projects/flex/til/spec/{feature}/concepts/*.md` 모두 읽기
- `~/Projects/flex/til/spec/{feature}/decisions/*.md` 모두 읽기 (있으면), **최신순 정렬**

추출 항목:
- 각 Concept의 SHOULD 항목 전체 목록
- 각 Concept의 SHOULD NOT 항목 전체 목록
- 각 Concept의 에지 케이스
- Decision Log의 변경 사항 (회귀 테스트 대상)

**Decision Log 충돌 처리:**
Decision Log는 최신순으로 유의미한 정보입니다. 동일 Concept/항목에 대해 여러 Decision Log가 존재하면 **최신 Decision이 우선**합니다. 이전 Decision은 무시하고 최신 기준으로 TC를 작성합니다.

#### 2-2. 구현 코드 분석

Concept과 관련된 코드를 탐색합니다:
- 컴포넌트 구성 및 사용자 인터랙션 흐름
- validation 로직, 에러 처리
- 상태 관리 (로딩, 에러, 빈 상태)
- API 호출 및 응답 처리

#### 2-3. Figma 디자인 분석 (선택)

Figma URL이 있으면:
```
mcp__figma__get_design_context({ fileKey, nodeId })
mcp__figma__get_screenshot({ fileKey, nodeId })
```

추출: UI 레이아웃, 인터랙션, 빈/에러/로딩 상태

#### 2-4. Linear 프로젝트 분석 (선택)

추가 Linear ID가 있으면:
```
mcp__linear-server__get_project({ id })
mcp__linear-server__list_issues({ projectId })
```

추출: 수용 기준, 이슈별 요구사항

### Phase 3: TC 설계

#### 3-1. 커버리지 매트릭스 구성

각 Concept의 SHOULD 항목을 기반으로 매트릭스를 구성합니다:

```markdown
| Concept | SHOULD 항목 | TC |
|---------|-------------|-----|
| table | 행 추가 시 빈 행이 하단에 삽입된다 | TC-TABLE-01 |
| table | 행 삭제 시 확인 다이얼로그가 표시된다 | TC-TABLE-02, TC-TABLE-03 |
| error-panel | 유효성 에러 시 에러 패널이 표시된다 | TC-ERR-01 |
```

**Decision Log 기반 회귀 TC:**
- 변경된 동작에 대한 회귀 테스트 TC 추가
- Decision Log에서 "변경 전 → 변경 후"를 검증하는 TC

**SHOULD NOT 기반 부정 TC:**
- 금지 동작이 실제로 발생하지 않는지 검증하는 TC

#### 3-2. 테스트 스위트 구성

관련된 TC를 Concept 기반으로 스위트를 그룹핑합니다:

```markdown
| Suite | ID 접두사 | Concept | TC 수 |
|-------|-----------|---------|-------|
| 테이블 기본 동작 | TC-TABLE | table | N개 |
| 에러 처리 | TC-ERR | error-panel | N개 |
| 회귀 테스트 | TC-REG | 여러 concept | N개 |
```

#### 3-3. TC 작성

각 TC는 아래 형식을 따릅니다:

```markdown
### TC-{SUITE}-{번호}: {TC 제목}

- **Concept**: [{concept-name}](./concepts/{concept-name}.md)
- **사전조건**: [필요한 상태/데이터]
- **절차**:
  1. [구체적인 액션] [selector: ...]
  2. [구체적인 액션] [selector: ...]
- **기대결과**: [검증 항목]
- **결과**: PASS / FAIL / SKIP
```

**TC 작성 규칙:**
- TC ID: `TC-{SUITE_PREFIX}-{번호}` (예: TC-TABLE-01)
- 절차는 Chrome DevTools MCP로 실행 가능한 수준으로 구체적 작성
- 기대 결과는 눈으로 검증 가능한 항목으로 작성
- 각 절차에 selector 힌트 포함: `[selector: button "저장"]`
- 각 TC가 어떤 Concept에서 도출되었는지 명시

### Phase 4: TC 리뷰

작성된 TC를 자체 리뷰합니다.

**리뷰 기준:**

| 기준 | 확인 내용 |
|------|-----------|
| **커버리지** | 모든 SHOULD 항목이 TC로 커버되는지 |
| **SHOULD NOT** | 금지 동작에 대한 부정 TC가 있는지 |
| **회귀** | Decision Log 변경사항에 대한 TC가 있는지 |
| **구체성** | 절차가 실행 가능한 수준인지 |
| **독립성** | 각 TC가 독립적으로 실행 가능한지 |
| **에지 케이스** | Concept의 에지 케이스가 TC에 반영되었는지 |

리뷰 결과를 사용자에게 보여주고 피드백을 받습니다.

### Phase 5: TC 저장

사용자에게 저장 방식을 확인합니다:

**Option A: Notion에 저장**
```
mcp__notion__notion-create-pages({
  parentPageUrl: "<parent-url>",
  pages: [{ title: "[기능명] QA TC", content: "<TC 전체>" }]
})
```

**Option B: 로컬 파일로 저장**
`~/Projects/flex/til/spec/{feature-name}/TC.md` 경로에 저장합니다.
형식: `templates/TC.md` 참조

## 사용할 MCP 도구

| 도구 | 용도 |
|------|------|
| Glob / Grep / Read | 코드 분석, 스펙 로드 |
| `mcp__figma__get_design_context` | Figma 디자인 분석 |
| `mcp__figma__get_screenshot` | Figma 스크린샷 |
| `mcp__linear-server__get_project` | Linear 프로젝트 정보 |
| `mcp__linear-server__list_issues` | 프로젝트 이슈 목록 |
| `mcp__notion__notion-fetch` | Notion 문서 읽기 |
| `mcp__notion__notion-create-pages` | Notion에 TC 저장 |

## 중요 사항

- **언어**: TC 문서는 한국어로 작성
- **Concept 기반 커버리지**: SHOULD 항목 100% 커버리지 목표
- **추적성**: 각 TC → Concept → SHOULD 항목 추적 가능
- **실행 가능성**: `run-qa` 스킬 또는 수동 QA가 바로 실행 가능한 수준
- **selector 힌트**: Chrome MCP로 요소를 찾기 쉽도록 포함

## 에러 처리

- 스펙 없음: `/drill:plan` 실행 안내
- Figma 접근 불가: 코드 기반으로 TC 작성
- Linear 접근 불가: spec 기반으로 TC 작성
- Concept에 SHOULD가 부족: 사용자에게 `/drill:plan`으로 보강 안내
