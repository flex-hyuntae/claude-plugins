---
name: ship
description: 티켓 여러 개를 받아 의존 순서대로 draft PR을 batch 생성합니다. 독립 티켓은 병렬, 의존 체인은 stacked.
disable-model-invocation: true
argument-hint: "<ticket-ids>"
---

# Ship

티켓 N개 → 의존 그래프 → worktree + `/drill:write` + 자동 커밋 분할 + draft PR batch 생성.

## Workflow

### 1. 의존 분석

`drill-deps` 에이전트 호출:
- 입력: ticket_ids + base_branch (기본: 현재 브랜치)
- 출력: independent + chain + 브랜치명 리포트

### 2. 계획 확인

리포트 요약 표시 (티켓 수, 브랜치, base 매핑, PR 개수) → AskUserQuestion: 진행 / 취소.

확인되면 이후 사용자 질문 없음 — 완료까지 자동.

### 3. 실행 순서

1. **Independent 먼저** (병렬 순서 의미 없음, 순차 실행)
2. **각 Chain** (위상정렬 순서로 순차)

### 4. 티켓별 처리

각 티켓:

1. **Linear 상태 전환**: `mcp__linear-server__save_issue`로 해당 티켓 상태를 `In Progress`로 변경. (이미 In Progress면 skip)
2. **Worktree 생성**
   - 경로: `../<current-repo-name>-<branch-slug>`
   - `git worktree add <path> -b <branch> <base>`
3. 해당 worktree로 `cd`
4. **`/drill:write {ticket}` 호출** — batch 모드 플래그 (위치 선정·커밋 질문 생략, 티켓 구현 가이드에 따라 자율 판단)
5. **커밋 분할** (5절)
6. **푸시**: `git push -u origin <branch>`
7. **Draft PR**: `gh pr create --draft --base <base> --title "<conv-commit>" --body "<템플릿에 따른 요약 + 티켓 링크>"` 또는 `mcp__github__create_pull_request` 로 생성
8. PR URL 기록
9. 원래 worktree로 복귀

실패 시: 해당 티켓 중단 + 리포트에 실패 기록, 다음 티켓 계속. 단, **chain 내부에서 중단되면 이후 티켓은 skip** (base가 만들어지지 않았으므로).

### 5. 커밋 분할

**PR 단위 ≠ 커밋 단위.** 한 PR 안에 여러 atomic 커밋을 두는 것이 기본. 커밋 하나당 독립적으로 이해되는 단일 목적을 갖는다.

다음 두 단계로 분할한다.

#### 5.1 카테고리 기반 기본 분할

`git status` 로 변경 파일 확인 후 다음 순서로 파일 그룹핑:

1. **타입·모델** (`models/`, `types/`, `*.types.ts`)
2. **유틸·헬퍼** (`utils/`, `helpers/`, `lib/`)
3. **서비스·훅·API** (`hooks/`, `services/`, `api/`, `queries/`)
4. **컴포넌트** (`components/`, `*.tsx` 중 화면·UI)
5. **테스트** (`*.spec.ts`, `*.test.tsx`, `__tests__/`)
6. **잔여** (스타일·설정·기타)

각 그룹에 대해:
- 해당 파일만 `git add`
- `yarn turbo run type-check --filter=@flex-apps/<pkg>` + `lint` 실행
- 통과 → Conventional Commit (`feat(scope): ...` / `refactor(scope): ...`)
- 실패 → 다음 그룹과 병합 후 재시도

빈 그룹은 건너뜀. `<pkg>` 는 변경 파일들의 가장 가까운 `package.json` name 에서 추출.

#### 5.2 논리 단위 재분할 (권장)

5.1이 파일 의존성으로 하나의 커밋으로 수렴하거나, 파일 카테고리는 같지만 목적이 다른 변경이 섞여 있으면 다음 기준으로 **수동 분할**한다:

- **리네임/이동 vs 신규 로직** — 먼저 이름·위치 정리 커밋, 그 위에 로직 변경 커밋
- **공용 모듈 신규 vs 소비처 연결** — 공용 모듈 커밋 먼저, 소비처 커밋 나중 (각각 type-check 통과 가능해야)
- **한 PR 안에 기능 단위가 여러 개** — 단위별 커밋 (예: 모달 컴포넌트 추가 / 상세 페이지에 모달 연결)
- **파일 스타일 포맷팅 (yarn format 등)** — 기능 커밋과 섞지 않는다. 별도 chore 커밋 또는 작업 파일만 포맷

각 논리 단위 커밋도 type-check/lint 통과를 목표로 한다. 의존성 때문에 개별 통과가 불가능하면 병합하되, "병합 불가피성"이 명확할 때만.

#### 5.3 실패 처리

전체 병합에도 type-check/lint 실패 → 강제 1커밋 + PR 본문에 경고 표기.

사용자 질문 없음.

### 6. 최종 리포트

````markdown
# Ship 완료

## PR 목록
| # | Ticket | Branch | Base | PR |
|---|--------|--------|------|-----|
| 1 | FLEX-123 | feat/... | develop | #456 |
| 2 | FLEX-124 | feat/... | feat/flex-123-... | #457 |

## Worktree
(경로 목록 — 피드백 반영 후 정리용)

## 실패 (있을 때만)
- FLEX-125: /drill:write 실패 — {이유}

## 수집된 [메모] (있을 때만)
- (대상 티켓/영역) 메모 내용 요약 — 반영됨 / 보류
- ...
````

## 제약

- **모든 PR은 `--draft`**
- 티켓당 1 브랜치 + 1 worktree
- 커밋 분할은 완전 자동 (질문 없음), 단 atomic commit 지향 (5절)
- stacked 체인에서 앞 PR 머지 대기 없음 — base 브랜치에 바로 쌓음
- 각 티켓 시작 시 Linear status 를 `In Progress` 로 전환
- 한국어

## `[메모]` 태그 발화 처리

사용자가 `[메모]` 로 시작하는 발화를 보내면 **ship 진행을 중단시키지 않는 피드백**으로 취급한다.

- 현재 진행 중인 ship 세션 **완료 후 일괄 반영**이 기본 원칙. 메모는 TaskList 또는 내부 노트에 축적.
- 단, 메모 대상이 **지금 작업 중이거나 방금 끝낸 티켓 PR** 이고 해당 PR 안에서 반영 가능하다면 즉시 반영해도 된다 (사용자가 "이 PR 에도"를 명시하거나 문맥상 명확할 때).
- 최종 리포트의 "수집된 [메모]" 섹션에 전체 목록을 정리해 사용자가 후속 처리할 수 있게 한다.
- 메모를 발견하면 "반영함 / 보류" 여부를 명시하고 반영 위치(PR#, 파일)를 함께 기록.

## 에러

- 티켓 조회 실패 → drill-deps Warnings, 해당 티켓 제외
- /drill:write 실패 → 티켓 중단, chain이면 이후 티켓 skip
- type-check/lint 전체 병합에도 실패 → 강제 1커밋 + PR 본문 경고
- `gh pr create` 실패 → 브랜치는 푸시된 상태 유지, 리포트에 실패 기록
- worktree 생성 실패 (브랜치명 중복 등) → 티켓 중단

## 관련

- `/drill:prepare` 가 만든 티켓들을 batch로 처리하는 후속 스킬
- 개별 티켓만 처리할 땐 `/drill:write` 단독 사용
- PR 피드백 후 Spec 동기화는 `/drill:review` 로
