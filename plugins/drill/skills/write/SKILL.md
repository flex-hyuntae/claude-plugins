---
name: write
description: Linear 티켓을 받아 Spec/Concept 기반으로 코드를 작성합니다
disable-model-invocation: true
argument-hint: "[linear-issue-url|issue-id]"
---

# Write

Linear 티켓 하나를 받아 Spec/Concept과 구현 가이드를 기반으로 실제 코드를 작성합니다.
rules 규칙 적용은 `rules:write` 스킬이 자동으로 처리합니다 (rules 플러그인 필요).

## 인자

| 인자 | 동작 |
|------|------|
| Linear URL/ID (예: `CORE-1234`) | 해당 티켓 로드 → 코드 작성 |
| 인자 없음 | AskUserQuestion으로 티켓 확인 |

## Workflow

### Phase 1: 컨텍스트 로드

1. `mcp__linear-server__get_issue`로 티켓 로드
2. 티켓 description에서 관련 Concept 경로 추출 (`~/Projects/flex/til/spec/{feature}/concepts/{name}.md`)
3. Spec index 파일 + 관련 Concept 파일들 읽기
4. 티켓에서 확인할 정보:
   - **목표**: 이 티켓이 달성해야 할 것
   - **수용 기준**: Concept의 책임·에지 케이스에서 도출된 체크리스트
   - **구현 가이드**: 파일 경로, 함수명, 구현 방향
   - **코드 위치**: 수정/생성할 파일 목록

### Phase 2: 코드베이스 탐색 (인터랙티브)

티켓의 코드 위치와 구현 가이드를 기반으로 관련 파일을 탐색합니다.

1. glob/grep으로 관련 파일 검색
2. read로 핵심 파일 읽기
3. 기존 패턴, 유틸리티, 컴포넌트 확인 후 재사용 판단

**AskUserQuestion으로 적절한 위치를 찾을 때까지 반복 질문:**
- "이 컴포넌트는 `{path}`에 추가하는 게 맞을까요?"
- "기존 `{util}`을 재사용할까요, 새로 만들까요?"
- "이 로직은 `{file}`의 `{function}` 근처에 넣으면 될까요?"
- "이 타입은 `{models/file}`에 정의하면 될까요?"

사용자 확인을 받은 뒤 Phase 3로 진행합니다.

### Phase 3: 코드 작성 (반복)

수용 기준을 하나씩 충족시키며 코드를 작성합니다.

1. Concept의 책임·에지 케이스를 수용 기준으로 삼아 구현
2. 티켓의 구현 가이드 방향에 맞게 Edit/Write
3. `rules:write` 스킬이 자동으로 rules 규칙을 적용 (직접 로드하지 않음)

**작은 작업 단위 완료 후 커밋 여부를 AskUserQuestion으로 확인:**

```
{작업 내용}을 완료했습니다. 여기서 커밋할까요?
- 커밋
- 이어서 진행
```

- 커밋 → 커밋 실행 후 다음 작업 단위로 진행
- 이어서 진행 → 다음 작업 단위로 바로 진행

모든 수용 기준을 충족할 때까지 반복합니다.

### Phase 4: 검증

코드 작성 완료 후 검증합니다.

```bash
# Type check
yarn turbo run type-check --filter=@flex-apps/{package-name}

# Lint
yarn turbo run lint --filter=@flex-apps/{package-name}
```

- 에러가 있으면 수정
- 수정 후 재검증

### Phase 5: 완료

1. 변경 파일 목록 안내
2. 수용 기준 충족 여부 체크리스트 표시
3. drill state 업데이트 (오케스트레이션에서 실행된 경우)

```
✅ write 완료

변경 파일:
- path/to/file1.tsx (신규)
- path/to/file2.tsx (수정)

수용 기준:
- [x] 기준 1
- [x] 기준 2
- [x] 기준 3
```

## rules 플러그인 의존성

이 스킬은 `rules` 플러그인이 설치되어 있을 때 최대 효과를 발휘합니다.
`rules:write` 스킬(`disable-model-invocation: false`)이 코드 작성 시 자동으로 규칙을 참조합니다:

- **항상 적용**: `ts-no-any`, `ts-no-type-assertion`, `naming-conventions`
- **작업 대상에 따라**: `react/`, `styling/`, `structure/`, `accessibility/`, `testing/`

## 사용할 MCP 도구

| 도구 | 용도 |
|------|------|
| `mcp__linear-server__get_issue` | 티켓 상세 조회 |
| Glob / Grep / Read | 코드베이스 탐색 |
| Edit / Write | 코드 작성 |

## 중요 사항

- **티켓 단위**: 한 번에 하나의 티켓만 처리
- **언어**: 모든 커뮤니케이션은 한국어
- **인터랙티브**: 코드 위치 확인, 커밋 여부 등 사용자와 지속적으로 소통
- **확인**: 코드 작성 전 위치 확인, 작성 후 커밋 확인

## 에러 처리

- Linear 티켓 조회 실패: 티켓 URL/ID 재확인 요청
- Spec/Concept 없음: Concept 없이 티켓 정보만으로 진행하거나 `/drill:plan` 안내
- type-check/lint 실패: 에러 수정 후 재검증
