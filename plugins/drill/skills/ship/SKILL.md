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

1. **Worktree 생성**
   - 경로: `../<current-repo-name>-<branch-slug>`
   - `git worktree add <path> -b <branch> <base>`
2. 해당 worktree로 `cd`
3. **`/drill:write {ticket}` 호출** — batch 모드 플래그 (위치 선정·커밋 질문 생략, 티켓 구현 가이드에 따라 자율 판단)
4. **자동 커밋 분할** (5절)
5. **푸시**: `git push -u origin <branch>`
6. **Draft PR**: `gh pr create --draft --base <base> --title "<conv-commit>" --body "<요약 + 티켓 링크>"`
7. PR URL 기록
8. 원래 worktree로 복귀

실패 시: 해당 티켓 중단 + 리포트에 실패 기록, 다음 티켓 계속. 단, **chain 내부에서 중단되면 이후 티켓은 skip** (base가 만들어지지 않았으므로).

### 5. 자동 커밋 분할

write 완료 후 `git status`로 변경 파일 확인. 다음 순서로 파일 그룹핑:

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
- 전체 병합해도 실패 → 최종 1커밋 + PR 본문에 경고 표기

`<pkg>` 는 변경 파일들의 가장 가까운 `package.json` name 에서 추출.

빈 그룹은 건너뜀. 사용자 질문 없음.

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
````

## 제약

- **모든 PR은 `--draft`**
- 티켓당 1 브랜치 + 1 worktree
- 커밋 분할은 완전 자동 (질문 없음)
- stacked 체인에서 앞 PR 머지 대기 없음 — base 브랜치에 바로 쌓음
- 한국어

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
