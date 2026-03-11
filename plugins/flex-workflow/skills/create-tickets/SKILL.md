---
name: create-tickets
description: 스펙 문서를 기반으로 Linear 티켓을 자동 생성하고 리뷰합니다
disable-model-invocation: true
---

# Create Tickets

이 스킬은 deep-interview가 생성한 스펙 문서를 읽어 Linear 티켓을 자동 생성하고, 자체 리뷰를 수행합니다.

## Workflow

### Phase 1: 스펙 문서 로드

인자로 feature-name을 받거나, `spec/` 하위 디렉토리 목록에서 선택합니다.

```bash
# spec/ 하위 디렉토리 목록 확인
ls spec/
```

- `spec/{feature-name}/SPEC.md` 읽기
- `spec/{feature-name}/spec-N-*.md` 파일들 모두 읽기
- SPEC.md에서 Linear 티켓 테이블과 Specs 테이블 파싱

디렉토리가 없거나 SPEC.md가 없으면 사용자에게 안내:
- `/plan:deep-interview`를 먼저 실행하여 스펙 문서를 생성하세요

### Phase 2: Linear 프로젝트 설정

Linear 팀과 프로젝트 정보를 수집합니다.

1. **팀 선택**: `mcp__claude_ai_Linear__list_teams` → 사용자에게 팀 선택 요청
2. **프로젝트 선택** (선택적): `mcp__claude_ai_Linear__list_projects` → 연결할 프로젝트 선택
3. **라벨 목록**: `mcp__claude_ai_Linear__list_issue_labels` → 사용 가능한 라벨 캐싱
4. **상태값 목록**: `mcp__claude_ai_Linear__list_issue_statuses` → 사용 가능한 상태값 캐싱

### Phase 3: 티켓 분해 계획

스펙 파일들을 분석하여 티켓 분해안을 작성합니다.

**최소 분해 단위 (필수 3카테고리)**:

| 순서 | 카테고리 | 설명 |
|------|----------|------|
| 1 | **Data modeling** | 데이터 모델/타입 정의, 스키마 설계 |
| 2 | **UI Component** | 컴포넌트 구현, 레이아웃, 인터랙션 |
| 3 | **API 적용** | API 연동, 데이터 페칭, 상태 관리 |

**분해 규칙:**
- 각 카테고리 내에서 추가로 작은 단위로 분해 가능
- 작업 순서: Data modeling → UI Component → API 적용
- 각 Spec 파일의 수용 기준을 하위 티켓의 수용 기준에 매핑
- 하나의 티켓은 최대 2일 이내 완료 가능한 크기

**사용자 확인:**

분해 계획을 테이블로 보여주고 확인받습니다:

```
| # | 부모/하위 | 카테고리 | 제목 | Spec 참조 | 예상 크기 |
|---|-----------|----------|------|-----------|-----------|
| 1 | 부모 | — | [기능명] 구현 | 전체 | — |
| 1-1 | 하위 | Data modeling | 타입 정의 | spec-1 | S |
| 1-2 | 하위 | UI Component | 목록 컴포넌트 | spec-2 | M |
| 1-3 | 하위 | API 적용 | API 연동 | spec-3 | M |
```

사용자가 수정을 요청하면 반영합니다.

### Phase 4: Linear 티켓 생성

확인된 계획에 따라 티켓을 생성합니다.

**생성 순서:**
1. **부모 이슈 먼저 생성**:
   ```
   mcp__claude_ai_Linear__save_issue({
     teamId: "<선택된 팀 ID>",
     title: "[기능명] 구현",
     description: "## 개요\n[SPEC.md 개요 섹션]\n\n## Specs\n[Specs 테이블 링크]",
     projectId: "<선택된 프로젝트 ID>",  // 선택적
     labelIds: [...]  // 해당하는 라벨
   })
   ```

2. **하위 이슈 순서대로 생성**:
   ```
   mcp__claude_ai_Linear__save_issue({
     teamId: "<선택된 팀 ID>",
     title: "[카테고리] [구체적 작업명]",
     description: "## 목표\n[작업 목표]\n\n## 수용 기준\n- [ ] [기준 1]\n- [ ] [기준 2]\n\n## 참조 Spec\n[spec 파일 내용 요약]",
     parentId: "<부모 이슈 ID>",
     projectId: "<선택된 프로젝트 ID>",  // 선택적
     labelIds: [...]
   })
   ```

**티켓 설명에 포함할 내용:**
- 목표 (해당 Spec에서 추출)
- 수용 기준 (체크리스트)
- 참조 Spec 요약
- 선행 작업 (의존성이 있는 경우)

### Phase 5: 티켓 리뷰

생성된 티켓들을 자체 리뷰합니다.

**리뷰 기준:**

| 기준 | 확인 내용 |
|------|-----------|
| **세분화** | 2일 이상 걸릴 티켓은 추가 분리 제안 |
| **순서** | 의존성 순서가 올바른지 검증 (Data modeling → UI → API) |
| **완전성** | 스펙의 모든 수용 기준이 티켓에 반영되었는지 확인 |
| **누락** | 스펙에는 있지만 티켓에 없는 항목 확인 |

**리뷰 결과를 사용자에게 보고:**

```
## 티켓 리뷰 결과

### 세분화
- [티켓 제목]: M 사이즈 → 적절
- [티켓 제목]: L 사이즈 → 분리 제안: [제안 내용]

### 순서
- 의존성 순서 OK / [문제점 설명]

### 완전성
- 스펙 대비 커버리지: N/M 수용 기준
- 누락 항목: [있으면 나열]
```

**사용자 피드백 반영:**
- 분리가 필요한 티켓: `mcp__claude_ai_Linear__save_issue`로 추가 하위 티켓 생성
- 수정이 필요한 티켓: `mcp__claude_ai_Linear__save_issue`로 기존 티켓 업데이트 (id 포함)
- 누락 항목: 새 티켓 생성

### Phase 6: SPEC.md 업데이트

생성된 Linear 티켓 정보를 SPEC.md에 반영합니다.

**Linear 티켓 테이블 업데이트:**

기존:
```markdown
## Linear 티켓
| 티켓 | 내용 | 상태 |
|------|------|------|
| [티켓 번호] | [설명] | [상태] |
```

업데이트 후:
```markdown
## Linear 티켓
| 티켓 | 내용 | 상태 |
|------|------|------|
| [TEAM-123](https://linear.app/...) | [부모 이슈 제목] | Backlog |
| [TEAM-124](https://linear.app/...) | [하위 이슈 1 제목] | Backlog |
| [TEAM-125](https://linear.app/...) | [하위 이슈 2 제목] | Backlog |
```

Edit 툴을 사용하여 SPEC.md의 티켓 테이블을 업데이트합니다.

## 사용할 MCP 도구

| 도구 | 용도 |
|------|------|
| `mcp__claude_ai_Linear__list_teams` | 팀 목록 조회 |
| `mcp__claude_ai_Linear__list_projects` | 프로젝트 목록 조회 |
| `mcp__claude_ai_Linear__list_issue_labels` | 라벨 목록 조회 |
| `mcp__claude_ai_Linear__list_issue_statuses` | 상태값 목록 조회 |
| `mcp__claude_ai_Linear__save_issue` | 이슈 생성/수정 |
| `mcp__claude_ai_Linear__create_issue_label` | 필요 시 라벨 생성 |

## 중요 사항

- **언어**: 모든 커뮤니케이션은 한국어로 진행
- **확인**: 티켓 생성 전 반드시 사용자 확인
- **순서**: Data modeling → UI Component → API 적용 순서 유지
- **크기**: 각 티켓은 최대 2일 이내 완료 가능한 크기
- **추적**: 생성된 모든 티켓 ID를 SPEC.md에 반영

## 에러 처리

- Linear API 실패 시: 에러 메시지 표시 후 재시도 또는 수동 생성 안내
- 스펙 문서 파싱 실패 시: 구조가 다른 부분 사용자에게 안내
- 라벨이 없는 경우: `create_issue_label`로 생성 제안
