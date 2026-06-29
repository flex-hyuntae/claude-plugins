---
name: ship
description: 'Linear 티켓 여러 개를 받아 의존 그래프를 만들고 worktree + /drill:write + 자동 커밋 분할로 draft PR을 batch 생성한다. 사용자가 "/drill:ship", "여러 티켓 PR 한번에", "stacked PR 생성", "batch PR"을 요청할 때 트리거. 독립 티켓은 병렬, 의존 체인은 stacked PR. 의존 분석은 drill-deps agent 활용. 정보가 부족한 티켓은 계획 확인 전에 /drill:prepare 강화 모드로 환류 후 진행.'
compatibility: 'Linear MCP + gh CLI + git worktree 지원 필수'
disable-model-invocation: true
argument-hint: "<ticket-ids>"
---

# Ship

티켓 N개 → 의존 그래프 → worktree + `/drill:write` + 자동 커밋 분할 + draft PR batch 생성.

## Workflow

### 1. 의존 분석

`drill-deps` 에이전트 호출. 입력: ticket_ids + base_branch(기본 현재 브랜치). 출력: independent + chain + 브랜치명 리포트.

### 1.5. 티켓 충분성 게이트 (prepare fallback)

각 티켓 본문을 prepare 재현성 게이트(`/drill:prepare` `§4.5`)로 판정해, write 가 모호성을 코드로 흡수하지 않도록 부족한 티켓을 먼저 환류한다. **반드시 §2 확인 직전에 둔다** — prepare 강화는 갭 인터뷰(AskUserQuestion)를 하는데 §2 이후로는 "질문 없음"을 보장하기 때문.

충분 판정 (티켓마다 자문):
- [ ] 변경 위치(파일/컴포넌트) 특정 — 신규/수정 표시 또는 Figma·티켓으로 자명
- [ ] 변경 명세 또는 시그니처·기존 패턴 포인터(`file:line`) 존재
- [ ] 각 수용 기준이 변경 명세 항목으로 추적됨
- [ ] 남은 모호함이 §미정 에 명시됨 (숨은 추정 없음)

분기: **충분** → §4 진행. **부족** → `/drill:prepare {ticket}` 강화 모드 인라인 실행, 갭 인터뷰는 여기서 전부 소진. 강화로 §의존이 바뀌면 §1 재실행, 아니면 §1 유지.

**과한 환류 금지** — 카피 한 줄·토큰/패딩 수치·outline↔solid 등 자명한 QA 폴리시는 변경 위치만 특정되면 시그니처/패턴 포인터가 비어도 충분으로 본다. 게이트는 write 가 설계를 떠안을 티켓만 거른다.

### 2. 계획 확인

리포트 요약(티켓 수, 브랜치, base 매핑, PR 개수, §1.5 강화 티켓) → AskUserQuestion: 진행 / 취소. 확인 후 질문 없음 — 완료까지 자동.

### 3. 실행 순서

Independent 먼저(순차) → 각 Chain(위상정렬 순).

### 4. 티켓별 처리

1. **Linear In Progress 전환** (`save_issue`, 이미면 skip)
2. **Worktree**: `git worktree add ../<repo>-<branch-slug> -b <branch> <base>` → 진입
3. **`/drill:write {ticket}`** — batch 모드(커밋 질문 생략, §구현 설계 따라 작성)
4. **커밋 분할** (§5)
5. **푸시**: `git push -u origin <branch>`
6. **Draft PR**: `gh pr create --draft --base <base> --title "<conv-commit>" --body "<요약+티켓 링크>"` (또는 `mcp__github__create_pull_request`)
7. PR URL 기록 → 원래 worktree 복귀

실패 시 해당 티켓 중단·기록 후 다음 계속. 단 **chain 내부 중단이면 이후 티켓 skip** (base 미생성).

### 5. 커밋 분할

**PR 단위 ≠ 커밋 단위.** 한 PR 안에 단일 목적 atomic 커밋 여럿.

**5.1 카테고리 분할** — 순서대로 그룹핑 후 그룹별 `add` + `type-check`/`lint` + Conventional Commit. 통과 실패 시 다음 그룹과 병합 재시도.
타입·모델(`models/`,`*.types.ts`) → 유틸(`utils/`,`lib/`) → 서비스·훅·API(`hooks/`,`api/`,`queries/`) → 컴포넌트(`*.tsx`) → 테스트(`*.spec.*`,`__tests__/`) → 잔여(스타일·설정).

**5.2 논리 재분할** — 아래 중 하나라도 해당하면 5.1 결과를 재분할(모두 미해당이면 skip). 각 단위도 type-check/lint 통과 목표, 개별 통과 불가하면 병합.

| 진입 조건 | 재분할 |
|----------|--------|
| 커밋당 파일 3개 또는 150줄 초과 | 단일 목적 단위로 |
| 리네임(`R`) + 신규 로직 공존 | 이름 정리 → 로직 변경 |
| 공용 모듈 신규 + 소비처 연결 | 공용 먼저 → 소비처 나중 |
| 한 PR 에 기능 여러 개 | 단위별 |
| 메시지에 "and/및" 필요 | 메시지 단위로 |
| 포맷팅 변경 포함 | 별도 chore 분리 |

**5.3 실패** — 전체 병합도 실패 → 강제 1커밋 + PR 본문 경고 (질문 없음).

### 6. 최종 리포트

````markdown
# Ship 완료

## PR 목록
| # | Ticket | Branch | Base | PR |
|---|--------|--------|------|-----|

## Worktree
(경로 목록 — 정리용)

## 강화된 티켓 / 실패 / 수집된 [메모] (각각 있을 때만)
- ...
````

## 제약

- 모든 PR `--draft`, 티켓당 1 브랜치 + 1 worktree
- 커밋 분할 완전 자동(질문 없음), atomic 지향(§5)
- stacked 체인은 머지 대기 없이 base 에 바로 쌓음
- 각 티켓 시작 시 Linear `In Progress` 전환
- 부족 티켓은 §1.5 에서 prepare 환류 — 모호성 코드 흡수 금지, 단 자명한 QA 폴리시는 환류 안 함
- 한국어

## `[메모]` 태그 발화

`[메모]` 로 시작하는 발화 = ship 중단 없는 피드백. 기본은 **세션 완료 후 일괄 반영**(TaskList 축적), 단 지금/방금 끝낸 티켓 PR 안에서 반영 가능하면 즉시. 발견 시 "반영/보류 + 위치(PR#·파일)" 기록, 최종 리포트에 정리.

## 에러

- 티켓 조회 실패 → drill-deps Warnings, 제외
- §1.5 강화 실패·게이트 미달 → 보고 후 제외 (모호성 코드 흡수 금지)
- /drill:write 실패 → 티켓 중단, chain 이면 이후 skip
- type-check/lint 전체 병합도 실패 → 강제 1커밋 + 본문 경고
- `gh pr create` 실패 → 브랜치는 푸시 유지, 실패 기록
- worktree 생성 실패(브랜치명 중복 등) → 티켓 중단

## 관련

- `/drill:prepare` 가 만든 티켓을 batch 처리하는 후속 스킬. 부족 티켓은 §1.5 에서 강화 모드로 환류
- 개별 티켓은 `/drill:write` 단독, PR 피드백 후 Spec 동기화는 `/drill:review`
