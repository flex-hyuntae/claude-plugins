---
name: run-qa
description: 작성된 TC를 Chrome DevTools MCP로 실행하여 QA 테스트를 수행하고 결과를 리포트합니다
disable-model-invocation: true
argument-hint: "[notion-tc-url|local-tc-path]"
---

# Run QA

이 스킬은 `write-tc` 스킬로 작성된 TC 문서를 기반으로 Chrome DevTools MCP를 사용하여 브라우저에서 QA 테스트를 자동 실행하고, 결과를 리포트합니다.

## Workflow

### Phase 1: TC 로드

인자로 TC 소스를 받거나, 사용자에게 확인합니다.

**TC 소스 (택 1):**
- Notion TC 문서 URL
- 로컬 TC 파일 경로 (예: `spec/{feature}/TC.md`)

**Notion에서 로드:**
```
mcp__claude_ai_Notion__notion-fetch({ url: "<tc-url>" })
```

**로컬 파일에서 로드:**
```
Read 도구로 TC.md 파일 읽기
```

TC 문서에서 파싱할 항목:
- 테스트 환경 (URL, feature flag, 계정)
- 테스트 스위트 목록
- 각 TC의 사전 조건, 절차, 기대 결과

### Phase 2: 테스트 환경 설정

#### 2-1. 브라우저 확인

Chrome DevTools MCP가 연결되어 있는지 확인합니다:

```
mcp__chrome-devtools__list_pages()
```

#### 2-2. 로그인

TC 문서의 테스트 계정 정보로 로그인합니다.
사용자에게 로그인 정보를 확인합니다:

1. 테스트 URL로 이동:
```
mcp__chrome-devtools__navigate_page({ url: "<test-url>" })
```

2. 이미 로그인되어 있는지 확인 (스크린샷으로):
```
mcp__chrome-devtools__take_screenshot()
```

3. 로그인이 필요하면:
   - 이메일 입력
   - 비밀번호 입력
   - 로그인 버튼 클릭
   - 로그인 완료 대기

#### 2-3. 테스트 페이지 이동

TC 문서에 명시된 테스트 대상 페이지로 이동합니다:
```
mcp__chrome-devtools__navigate_page({ url: "<app-url>" })
mcp__chrome-devtools__wait_for({ text: ["<페이지 로드 확인 텍스트>"] })
```

### Phase 3: TC 실행

각 스위트를 순서대로 실행합니다. 각 TC 실행 시:

#### 3-1. 사전 조건 충족

TC의 사전 조건을 확인하고 필요한 상태를 준비합니다:
- 모달 열기, 데이터 입력 등

#### 3-2. 절차 실행

TC의 각 절차를 Chrome MCP 도구로 실행합니다:

| TC 절차 동사 | Chrome MCP 도구 |
|-------------|-----------------|
| "클릭한다" | `mcp__chrome-devtools__click` |
| "더블 클릭한다" | `mcp__chrome-devtools__click({ dblClick: true })` |
| "입력한다" / "작성한다" | `mcp__chrome-devtools__fill` 또는 `mcp__chrome-devtools__type_text` |
| "키를 누른다" | `mcp__chrome-devtools__press_key` |
| "호버한다" | `mcp__chrome-devtools__hover` |
| "드래그한다" | `mcp__chrome-devtools__drag` |
| "이동한다" | `mcp__chrome-devtools__navigate_page` |
| "대기한다" | `mcp__chrome-devtools__wait_for` |
| "확인한다" / "검증한다" | `mcp__chrome-devtools__take_screenshot` + `mcp__chrome-devtools__take_snapshot` |

**요소 찾기 전략:**
1. TC에 `[selector: ...]` 힌트가 있으면 해당 정보를 우선 사용
2. `take_snapshot()`으로 페이지 DOM 트리 확인
3. 텍스트 내용, role, aria-label 기반으로 uid 매칭
4. 요소를 찾을 수 없으면 스크린샷을 찍고 사용자에게 확인 요청

#### 3-3. 기대 결과 검증

각 기대 결과 항목을 검증합니다:

1. **스크린샷 검증**: `take_screenshot()`으로 시각적 상태 확인
2. **DOM 검증**: `take_snapshot()`으로 텍스트, 요소 존재 여부 확인
3. **스크립트 검증**: `evaluate_script()`으로 값 비교, 개수 확인 등

```
// 예: 텍스트 존재 확인
mcp__chrome-devtools__evaluate_script({
  function: "() => document.body.innerText.includes('총 5개')"
})
```

#### 3-4. 결과 기록

각 TC의 결과를 기록합니다:
- **PASS**: 모든 기대 결과가 충족됨
- **FAIL**: 하나 이상의 기대 결과가 불충족
- **SKIP**: 사전 조건을 충족할 수 없거나, 기술적 제약으로 실행 불가
- **BLOCK**: 이전 TC 실패로 인해 실행 불가

FAIL인 경우:
- 실패 지점 스크린샷 저장
- 실패 원인 설명 기록
- 기대값 vs 실제값 비교

#### 3-5. 상태 복원

다음 TC를 위해 상태를 초기화합니다:
- 열린 모달/다이얼로그 닫기
- 필요시 페이지 새로고침
- 테스트 데이터 정리 (추가한 항목 삭제 등)

### Phase 4: 결과 리포트

모든 TC 실행이 끝나면 결과를 정리하여 리포트합니다.

**리포트 형식:**

```markdown
## QA 테스트 결과 리포트

### 요약
| 항목 | 값 |
|------|-----|
| 실행일 | {date} |
| 총 TC | N개 |
| PASS | X개 |
| FAIL | Y개 |
| SKIP | Z개 |
| 통과율 | X/N (%) |

### 스위트별 결과
| Suite | 총 TC | PASS | FAIL | SKIP |
|-------|-------|------|------|------|
| MODAL | 5 | 5 | 0 | 0 |
| ROW | 7 | 6 | 1 | 0 |
| ... | ... | ... | ... | ... |

### FAIL 상세
#### TC-ROW-03: [TC 제목]
- **실패 지점**: 절차 3단계
- **기대 결과**: [기대값]
- **실제 결과**: [실제값]
- **스크린샷**: [경로]
- **가능 원인**: [분석]

### SKIP 상세
#### TC-PASTE-01: [TC 제목]
- **사유**: 클립보드 접근 불가 (Chrome MCP 제약)

### 특이 사항
- [테스트 중 발견한 비정상 동작이나 주의 사항]
```

**리포트 저장:**
- 터미널에 요약 출력
- 상세 리포트는 사용자 요청 시 Notion에 저장:

```
mcp__claude_ai_Notion__notion-create-pages({
  parentPageUrl: "<parent-url>",
  pages: [{
    title: "[기능명] QA 결과 ({date})",
    content: "<리포트 markdown>"
  }]
})
```

## 사용할 MCP 도구

### Chrome DevTools (핵심)

| 도구 | 용도 |
|------|------|
| `mcp__chrome-devtools__navigate_page` | 페이지 이동 |
| `mcp__chrome-devtools__take_screenshot` | 시각적 검증, 증거 저장 |
| `mcp__chrome-devtools__take_snapshot` | DOM 트리 확인, 요소 uid 찾기 |
| `mcp__chrome-devtools__click` | 버튼/요소 클릭 |
| `mcp__chrome-devtools__fill` | 입력 필드에 값 입력 |
| `mcp__chrome-devtools__type_text` | 키보드로 텍스트 입력 |
| `mcp__chrome-devtools__press_key` | 키보드 단축키 (Enter, Escape, Tab 등) |
| `mcp__chrome-devtools__hover` | 호버 인터랙션 |
| `mcp__chrome-devtools__drag` | 드래그 앤 드롭 |
| `mcp__chrome-devtools__wait_for` | 텍스트 표시 대기 |
| `mcp__chrome-devtools__evaluate_script` | JavaScript 실행으로 값 검증 |
| `mcp__chrome-devtools__list_pages` | 브라우저 연결 확인 |

### Notion (TC 로드 및 결과 저장)

| 도구 | 용도 |
|------|------|
| `mcp__claude_ai_Notion__notion-fetch` | TC 문서 로드 |
| `mcp__claude_ai_Notion__notion-create-pages` | 결과 리포트 저장 |

## 중요 사항

- **언어**: 모든 리포트는 한국어로 작성
- **스크린샷**: 각 TC 실행 전후로 스크린샷 촬영 (FAIL 시 필수)
- **상태 복원**: TC 간 상태 오염 방지를 위해 매 TC 후 상태 초기화
- **타임아웃**: `wait_for` 사용 시 적절한 타임아웃 설정 (기본 5000ms)
- **요소 탐색**: snapshot의 uid를 사용하여 요소 클릭/입력 (텍스트 기반 uid는 신뢰도 낮음)
- **FAIL 시 계속 진행**: 한 TC가 FAIL이어도 다음 TC를 계속 실행 (BLOCK 조건이 아닌 한)
- **실시간 보고**: 각 TC 실행 결과를 즉시 사용자에게 출력 (전체 완료 후 요약도 별도 제공)
- **데이터 안전**: 테스트 데이터 추가 후 반드시 정리 (삭제). 기존 데이터는 수정/삭제 금지

## 에러 처리

- Chrome MCP 연결 실패: 브라우저 실행 및 DevTools 연결 확인 안내
- 로그인 실패: 계정 정보 재확인 요청
- 요소를 찾을 수 없음: 스크린샷 + snapshot 촬영 후 사용자에게 확인 요청
- 페이지 로딩 타임아웃: 새로고침 후 재시도 (최대 2회)
- 예상치 못한 다이얼로그: 스크린샷 촬영 후 사용자에게 대응 방법 확인

## 실행 불가능한 TC 유형

아래 유형의 TC는 Chrome MCP로 실행이 어려울 수 있습니다. SKIP 처리하고 사유를 기록합니다:

| 유형 | 사유 | 대안 |
|------|------|------|
| 클립보드 붙여넣기 | Chrome MCP에서 클립보드 접근 제한 | `evaluate_script`로 paste 이벤트 시뮬레이션 시도 |
| 파일 업로드 | 파일 선택 다이얼로그 제어 불가 | `upload_file` 도구 사용 시도 |
| 브라우저 탭 전환 | 탭 간 전환 제약 | `select_page`로 시도 |
| 네트워크 에러 시뮬레이션 | 네트워크 조건 제어 불가 | 수동 테스트 권장 |
