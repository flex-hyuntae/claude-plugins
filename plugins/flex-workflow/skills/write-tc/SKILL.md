---
name: write-tc
description: Linear 프로젝트, 테스트 대상 코드, Figma, 스펙 문서를 기반으로 QA 테스트 케이스를 작성합니다
disable-model-invocation: true
argument-hint: "[linear-project-id|notion-spec-url]"
---

# Write TC (Test Case)

이 스킬은 Linear 프로젝트, 테스트 대상 코드, Figma 디자인, 스펙 문서(Notion 또는 코드 내 deep-interview 스펙)를 종합 분석하여 체계적인 QA 테스트 케이스를 작성합니다.

## Workflow

### Phase 1: 소스 수집

사용자에게 아래 정보를 수집합니다. 인자로 URL이 주어지면 해당 단계를 건너뜁니다.

**필수 입력:**

1. **Linear 프로젝트**: 프로젝트 ID (예: `CORE-123`)
2. **테스트할 코드 위치**: 테스트 대상 코드 경로 (예: `apps/web/src/features/some-feature/`)
3. **테스트 대상 앱**: 테스트할 애플리케이션 URL (예: `http://flex.local.flexis.team:3000/...`)

**선택 입력 (있으면 더 정밀한 TC 작성 가능):**

4. **Figma 디자인**: 디자인 URL (있으면 UI/UX TC 보강)
5. **Notion 스펙 문서**: 스펙 문서 URL (있으면 수용 기준 기반 TC 작성)
6. **Feature flag**: 테스트에 필요한 feature flag 이름

### Phase 2: 소스 분석

수집한 소스를 모두 분석합니다. 각 소스를 **병렬로** 분석하여 효율을 높입니다.

#### 2-1. Linear 프로젝트 분석

```
mcp__claude_ai_Linear__get_project({ id: "<project-id>" })
mcp__claude_ai_Linear__list_issues({ projectId: "<project-id>" })
```

추출 항목:
- 프로젝트 설명 및 목표
- 하위 이슈 목록 및 각 이슈의 수용 기준
- 완료된 이슈와 미완료 이슈 구분
- 관련 PR 링크

#### 2-2. 테스트 대상 코드 분석

사용자가 지정한 코드 경로를 Explore agent로 분석합니다. 코드는 이미 base 브랜치에 머지된 상태이므로 diff가 아닌 현재 코드를 직접 읽습니다:

- 컴포넌트 구성 및 사용자 인터랙션 흐름
- validation 로직, 에러 처리
- 상태 관리 (isDirty, isLoading 등)
- API 호출 및 응답 처리
- deep-interview 기반 스펙 문서가 코드 내에 존재하면 함께 분석 (예: `spec/`, `docs/`, `*.spec.md` 등)

#### 2-3. Figma 디자인 분석 (선택)

Figma URL이 있으면:

```
mcp__figma__get_design_context({ fileKey: "<key>", nodeId: "<node>" })
mcp__figma__get_screenshot({ fileKey: "<key>", nodeId: "<node>" })
```

추출 항목:
- UI 레이아웃, 컴포넌트 구성
- 인터랙션 흐름 (hover, click, focus 등)
- 빈 상태, 에러 상태, 로딩 상태 디자인
- 반응형 동작

#### 2-4. 스펙 문서 분석 (선택)

두 가지 스펙 소스를 확인합니다:

**A. 코드 내 스펙 (deep-interview 기반)**

2-2에서 발견한 코드 내 스펙 문서를 분석합니다. deep-interview를 통해 작성된 상세 스펙이 코드 레벨에 존재할 수 있습니다.

**B. Notion 스펙 문서**

Notion URL이 있으면:

```
mcp__claude_ai_Notion__notion-fetch({ url: "<notion-url>" })
```

추출 항목:
- 기능 요구사항
- 수용 기준
- Edge case 정의
- 비즈니스 규칙

### Phase 3: TC 설계

분석 결과를 종합하여 TC를 설계합니다.

#### 3-1. 테스트 범위 정의

변경 사항을 기반으로 테스트 범위를 정합니다:

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| **기본 동작** | Happy path 기능 동작 | 모달 열기/닫기, CRUD |
| **UI/UX** | 디자인 명세 일치 | 레이아웃, 애니메이션, 빈 상태 |
| **Validation** | 입력값 검증 | 필수값, 길이 제한, 중복 체크 |
| **에러 처리** | 에러 상황 대응 | 서버 에러, 네트워크 에러 |
| **Edge Case** | 경계 조건 | 대량 데이터, 동시 조작, 빈 목록 |
| **접근성** | 키보드/스크린리더 | Tab 이동, Escape 닫기 |

#### 3-2. 테스트 스위트 구성

관련된 TC를 스위트로 그룹핑합니다:

```markdown
| Suite | ID 접두사 | 범위 | TC 수 |
|-------|-----------|------|-------|
| 모달 기본 동작 | TC-MODAL | 열기, 닫기, 초기 상태 | N개 |
| 행 편집 | TC-ROW | 추가, 수정, 삭제 | N개 |
| Validation | TC-VALID | 클라이언트 검증 | N개 |
| ... | ... | ... | ... |
```

#### 3-3. TC 작성

각 TC는 아래 형식을 따릅니다:

```markdown
### TC-{SUITE}-{번호}: {TC 제목}

**사전 조건:**
- [필요한 상태/데이터]

**절차:**
1. [구체적인 액션]
2. [구체적인 액션]
3. ...

**기대 결과:**
- [검증 항목 1]
- [검증 항목 2]

**비고:** [특이사항, 관련 이슈 등]
```

**TC 작성 규칙:**
- TC ID는 `TC-{SUITE_PREFIX}-{번호}` 형식 (예: TC-MODAL-01, TC-ROW-03)
- 절차는 Chrome DevTools MCP로 실행 가능한 수준으로 구체적으로 작성
  - "XX 버튼을 클릭한다" (O) vs "기능을 테스트한다" (X)
- 기대 결과는 눈으로 검증 가능한 항목으로 작성
  - "총 N개 텍스트가 표시된다" (O) vs "정상 동작한다" (X)
- 각 절차 단계에서 사용할 selector 힌트를 `[selector: ...]`로 남긴다
  - 예: `1. "설정 저장" 버튼을 클릭한다 [selector: button "설정 저장"]`

### Phase 4: TC 리뷰

작성된 TC를 자체 리뷰합니다.

**리뷰 기준:**

| 기준 | 확인 내용 |
|------|-----------|
| **커버리지** | 수용 기준이 모두 TC로 커버되는지 |
| **구체성** | 절차가 Chrome MCP로 실행 가능한 수준인지 |
| **독립성** | 각 TC가 독립적으로 실행 가능한지 |
| **Edge Case** | 경계 조건, 에러 상황이 포함되었는지 |
| **중복** | 불필요한 중복 TC가 없는지 |

리뷰 결과를 사용자에게 보여주고 피드백을 받습니다:

```markdown
## TC 리뷰 결과

- 총 TC 수: N개 (M개 스위트)
- 수용 기준 커버리지: X/Y
- 누락된 항목: [있으면 나열]
- 추가 권장 TC: [있으면 나열]
```

사용자가 수정을 요청하면 반영합니다.

### Phase 5: TC 문서 저장

사용자에게 저장 방식을 확인합니다:

**Option A: Notion에 저장** (권장)

```
mcp__claude_ai_Notion__notion-create-pages({
  parentPageUrl: "<parent-url>",
  pages: [{
    title: "[기능명] QA TC",
    content: "<TC 전체 내용 markdown>"
  }]
})
```

**Option B: 로컬 파일로 저장**

`spec/{feature-name}/TC.md` 경로에 저장합니다.

**TC 문서 최종 구조:**

```markdown
# [기능명] QA Test Cases

## 개요
- Linear 프로젝트: [링크]
- Figma: [링크]
- 스펙 문서: [링크]
- 작성일: {date}
- 총 TC: N개 (M개 스위트)

## 테스트 환경
- URL: {app-url}
- Feature Flag: {flag-name}
- 계정: [테스트 계정 정보]

## 테스트 스위트 요약
| Suite | ID | 범위 | TC 수 |
|-------|----|------|-------|
| ... | ... | ... | ... |

## TC 상세

### Suite 1: [스위트명]
[TC 목록]

### Suite 2: [스위트명]
[TC 목록]
...
```

## 사용할 MCP 도구

| 도구 | 용도 |
|------|------|
| `mcp__claude_ai_Linear__get_project` | Linear 프로젝트 정보 조회 |
| `mcp__claude_ai_Linear__list_issues` | 프로젝트 하위 이슈 목록 조회 |
| `mcp__figma__get_design_context` | Figma 디자인 분석 |
| `mcp__figma__get_screenshot` | Figma 디자인 스크린샷 |
| `mcp__claude_ai_Notion__notion-fetch` | Notion 스펙 문서 읽기 |
| `mcp__claude_ai_Notion__notion-create-pages` | Notion에 TC 저장 |

## 중요 사항

- **언어**: TC 문서는 한국어로 작성
- **구체성**: 절차는 `run-qa` 스킬이 Chrome MCP로 바로 실행할 수 있을 정도로 구체적으로 작성
- **ID 체계**: TC-{SUITE}-{번호} 형식 유지 (예: TC-MODAL-01)
- **독립성**: 각 TC는 사전 조건만 충족되면 독립 실행 가능
- **추적성**: 각 TC가 어떤 수용 기준/스펙에서 도출되었는지 명시
- **실행 가능성**: "클릭", "입력", "확인" 같은 구체적 동사 사용
- **selector 힌트**: `run-qa` 스킬이 요소를 찾기 쉽도록 selector 힌트 포함

## 에러 처리

- Linear 프로젝트 조회 실패: 프로젝트 ID 확인 요청
- Figma 접근 불가: Figma 없이 코드 기반으로 TC 작성 진행
- Notion 접근 불가: Notion 없이 다른 소스 기반으로 TC 작성 진행
- 코드 경로에 파일 없음: 사용자에게 코드 위치 재확인 요청
