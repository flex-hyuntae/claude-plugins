---
name: enrich-ticket
description: QA 티켓을 인터뷰와 자동 탐색으로 구조화된 형식으로 강화합니다
disable-model-invocation: true
argument-hint: "[linear-issue-url|issue-id]"
---

# Enrich Ticket

PM/PD가 QA 중 생성한 Linear 티켓을 분석하고, Figma 디자인 조회 · 코드베이스 탐색 · 개발자 인터뷰를 통해 누락된 맥락을 수집하여 구조화된 형식으로 티켓 설명을 업데이트합니다.

## Workflow

### Phase 1: 티켓 로드 및 분석

**인자 파싱:**
- Linear URL: `https://linear.app/{team}/issue/{ID}/...` → ID 추출
- 짧은 식별자: `CORE-1234` → 그대로 사용
- 인자 없음: AskUserQuestion으로 티켓 URL 또는 ID 요청

**티켓 조회:**

```
mcp__claude_ai_Linear__get_issue({ id: "<issue-id>" })
mcp__claude_ai_Linear__list_comments({ issueId: "<issue-id>" })
```

**기존 정보 분석 — 다음 항목이 이미 존재하는지 판단:**

| 항목 | 확인 대상 |
|------|-----------|
| 증상 | 제목, 설명 텍스트 |
| 재현 경로 | 설명/코멘트에 단계별 기술이 있는지 |
| 스크린샷/영상 | 이미지 URL, 첨부파일 링크 |
| Figma URL | 설명/코멘트에서 `figma.com` URL |
| 기대 동작 | 기대 동작에 대한 기술 여부 |
| 컴포넌트/페이지명 | 설명에서 UI 요소 키워드 |
| 수용 기준 | 체크리스트 또는 AC 기술 여부 |

**갭 목록 생성:** 빠진 항목들을 식별하여 Phase 3 인터뷰에서 채울 대상 결정.

### Phase 2: 자동 컨텍스트 수집

#### 2-1. Figma 디자인 조회 (Figma URL 발견 시)

```
mcp__figma__get_design_context({
  fileKey: "<key>",
  nodeId: "<node>",
  clientFrameworks: "react",
  clientLanguages: "typescript"
})

mcp__figma__get_screenshot({
  fileKey: "<key>",
  nodeId: "<node>"
})
```

- Figma URL에서 `fileKey`와 `nodeId` 파싱
  - `figma.com/design/:fileKey/:fileName?node-id=:nodeId` → nodeId의 `-`를 `:`로 변환
- 조회 결과에서 추출:
  - TO-BE 섹션용 기대 UI 설명
  - 컴포넌트명 → Phase 2-2 코드 탐색 키워드로 활용
- 조회 실패 시: Phase 3에서 사용자에게 기대 동작을 직접 기술하도록 요청

#### 2-2. 코드베이스 탐색 (항상 실행)

티켓 제목/설명/Figma 결과에서 키워드를 추출하여 코드를 검색합니다.

**키워드 추출 대상:**
- 컴포넌트명 (예: `GoalModal`, `EvaluationTable`)
- 페이지/라우트명 (예: `/goals`, `/evaluations`)
- 기능 키워드 (예: `objective`, `review`, `typing`)

**검색:**
```
Glob: **/*{keyword}*.tsx
Grep: pattern="{ComponentName}", type="tsx"
```

- 핵심 파일 3-5개를 Read하여 파일 경로 + 간단한 역할 정리
- 검색 결과 없으면 Phase 3에서 사용자에게 코드 위치 질문
- 매치가 너무 많으면 (20+) 앱/모듈 범위를 좁히기 위해 사용자에게 질문

### Phase 3: 갭 인터뷰

Phase 1-2에서 채워지지 않은 항목만 질문한다.
AskUserQuestion 사용, 한국어. 질문 갯수 제약 없음 — 필요한 만큼 자유롭게 질문한다.

**질문 우선순위** (이미 있는 정보는 건너뜀):

| 우선순위 | 질문 | 건너뛰는 조건 |
|----------|------|---------------|
| 1 | **재현 경로** — 어떤 경로로 이 화면에 도달하고 어떤 조건에서 발생하나요? | 티켓에 재현 단계 있음 |
| 2 | **기대 동작** — 피그마/스펙 대비 어떤 동작이 기대되나요? | Figma 조회 성공 또는 기대동작 기술됨 |
| 3 | **영향 범위** — 같은 컴포넌트를 쓰는 다른 곳에도 영향이 있나요? | 코드 탐색으로 범위 명확 |
| 4 | **코드 위치 확인** — [탐색 결과 제시] 이 파일들이 관련 코드가 맞나요? | 코드 탐색 결과가 모호할 때만 질문 |
| 5 | **특수 조건** — 특정 데이터/권한/feature flag 등 재현에 필요한 조건이 있나요? | 거의 항상 질문 |
| 6 | **원인 추정** — 혹시 원인에 대한 추정이 있으신가요? | 선택적 — 있으면 포함 |
| 7 | **수용 기준** — 수정 완료 판단 기준은 무엇인가요? | 티켓에 AC 있음 |

**인터뷰 진행 방식:**
- 수집 완료된 항목은 건너뛰고 부족한 항목만 질문
- 갭이 많으면 한 번에 여러 질문을 묶어 진행
- 갭이 적으면 핵심 질문만 빠르게 진행
- 사용자 답변에 따라 follow-up 질문 생성

**동적 후속 처리:**
- 인터뷰 중 Figma URL 언급 → 즉시 Phase 2-1 실행
- 파일 경로 언급 → 즉시 Read
- 관련 티켓 언급 → 참고 섹션에 기록

**종료 조건:**
- 모든 갭 항목이 충족됨
- 사용자가 "충분해" 등으로 종료 의사 표시
- 최대 5라운드

### Phase 4: 템플릿 조합

수집한 모든 정보를 아래 템플릿으로 조합합니다.

```markdown
# AS-IS
- **증상**: [버그 증상 — 무엇이 잘못되었는지]
- **재현 경로**:
  1. [step 1]
  2. [step 2]
  3. [step 3]
- **스크린샷/영상**: [PM/PD 원본 첨부 포함 — 이미지 URL 그대로 유지]

# TO-BE
- **기대 동작**: [올바른 동작 설명]
- **피그마 참조**: [Figma URL + 기대되는 UI 간단 설명]

# 영향 범위
- **페이지/컴포넌트**: [영향 받는 페이지, 컴포넌트 목록]
- **관련 기능**: [연관된 기능들]

# 코드 위치
- `path/to/component.tsx` — [역할 설명]
- `path/to/hook.ts` — [역할 설명]
- `path/to/utils.ts` — [역할 설명]

# 구현 가이드
- [어떤 파일에서 어떤 함수/컴포넌트를 수정해야 하는지 구체적으로 기술]
- [예: `MessageList.tsx`에서 `useEffect` 내 `subscribeToTask` 호출 추가]
- [예: `processA2AStream`의 기존 이벤트 처리 로직이 그대로 적용됨]
- [예: `isNewContext: false`로 기존 context에 연결]

# 원인 추정
- **가설**: [개발자의 원인 추정]
- **확인 포인트**: [검증할 코드 위치/조건]

# 수용 기준
- [ ] [기준 1]
- [ ] [기준 2]
- [ ] [기준 3]

# 참고
- **피그마**: [Figma link]
- **관련 티켓**: [related ticket links]
- **기타**: [스펙 문서, API 엔드포인트 등]
```

**조합 규칙:**
- PM/PD 원본 스크린샷/영상은 반드시 보존 — AS-IS 섹션에 이미지 URL 그대로 통합
- Phase 3에서 "원인 추정" 답변이 없으면 해당 섹션 제거
- 빈 섹션은 포함하지 않음
- 코드 위치의 파일 경로는 프로젝트 루트 기준 상대 경로 사용

**사용자 확인:**
- 조합된 템플릿 초안을 사용자에게 보여줌
- "이 내용으로 Linear 티켓을 업데이트할까요? 수정할 부분이 있으면 알려주세요."
- 수정 요청 시 반영 후 재확인

### Phase 5: 티켓 업데이트

사용자 승인 후 Linear 티켓을 업데이트합니다.

**description 교체:**
```
mcp__claude_ai_Linear__save_issue({
  id: "<issue-id>",
  description: "<조합된 템플릿>"
})
```

**완료 안내:**
- 티켓 URL 제공
- 업데이트된 내용 요약

## 사용할 MCP 도구

| 도구 | Phase | 용도 |
|------|-------|------|
| `mcp__claude_ai_Linear__get_issue` | 1 | 티켓 상세 조회 |
| `mcp__claude_ai_Linear__list_comments` | 1 | 코멘트 조회 (추가 맥락) |
| `mcp__figma__get_design_context` | 2 | 피그마 디자인 컨텍스트 조회 |
| `mcp__figma__get_screenshot` | 2 | 피그마 스크린샷 조회 |
| Glob / Grep | 2 | 코드베이스 파일 검색 |
| Read | 2 | 관련 소스 파일 읽기 |
| `mcp__claude_ai_Linear__save_issue` | 5 | 티켓 description 업데이트 |

## 중요 사항

- **코드 수정 금지**: 이 스킬은 Linear 티켓 description만 업데이트한다. 코드베이스 탐색은 원인 추정과 코드 위치 파악 용도로만 수행하며, 절대로 소스 코드를 수정하거나 구현하지 않는다.
- **언어**: 모든 커뮤니케이션은 한국어로 진행
- **원본 보존**: PM/PD가 첨부한 스크린샷/영상 URL은 반드시 유지
- **스마트 인터뷰**: 이미 수집된 정보는 다시 묻지 않음
- **확인**: 티켓 업데이트 전 반드시 사용자 확인

## 에러 처리

- **이슈 조회 실패**: ID 확인 요청, 팀명 확인
- **Figma 조회 실패**: 기대 동작을 인터뷰에서 직접 수집
- **코드 탐색 결과 없음**: 사용자에게 코드 위치 직접 질문
- **Linear 업데이트 실패**: 에러 메시지 표시, 템플릿 텍스트를 직접 제공하여 수동 복사 가능하도록 안내
