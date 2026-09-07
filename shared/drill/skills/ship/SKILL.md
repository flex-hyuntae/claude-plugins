---
name: ship
description: 'Linear 티켓 여러 개를 받아 의존 그래프를 만들고 worktree + /drill:write + 자동 커밋 분할로 draft PR을 batch 생성한다. 사용자가 "/drill:ship", "여러 티켓 PR 한번에", "stacked PR 생성", "batch PR"을 요청할 때 트리거. 독립 티켓은 병렬, 의존 체인은 stacked PR. 의존 분석은 drill-deps agent 활용. 정보가 부족한 티켓은 계획 확인 전에 /drill:prepare 강화 모드로 먼저 보강한다.'
compatibility: 'Linear MCP + gh CLI + git worktree 지원 필수. gh stack extension 권장 (chain 을 GitHub 네이티브 stack 으로 등록 → 자동 restack)'
disable-model-invocation: true
argument-hint: "<ticket-ids>"
---

# Ship

티켓 N개 → 의존 그래프 → worktree + `/drill:write` + 자동 커밋 분할 + draft PR batch 생성.

## Workflow

### 1. 의존 분석

`drill-deps` 에이전트 호출. 입력: ticket_ids + base_branch(기본 현재 브랜치). 출력: independent + chain + 브랜치명 리포트.

**BE 레포면** 커밋·PR·브랜치 컨벤션을 `backend-guidelines-doc-loader` 로 로드해 따른다 (`references/STACK.md` §BE 컨벤션 위임). drill 기본값(Conventional Commit·`feat/<id>-<slug>`)과 다르면 그쪽이 우선.

### 2. 티켓 충분성 게이트 (prepare 선행)

ship 의 batch write 는 §3 확인 이후 무질문 → write 가 §Cascade 할 상황을 여기서 미리 닫는다. 판정 기준은 write 의 §Cascade 와 동일 — 티켓 §구현 설계가 제품 how·구현 how 를 닫고 있는가.

**판정은 읽기 전용이다 — 티켓 본문을 바꾸지 않는다.** 결과로 분기만 한다:

- **충분** → 그대로 §5 진행 (write 가 추가 질문 없이 작성).
- **부족** → `/drill:prepare` 강화 모드를 먼저 실행해 티켓을 채운다. 갭 인터뷰(AskUserQuestion)는 여기서 전부 끝낸다. 강화로 §의존(`blockedBy`/`relatedTo`)이 바뀌면 §1 재실행.

**자명한 QA 는 건너뛴다** — 카피 한 줄·토큰/패딩 수치·variant 교체(ghost↔outline 등)처럼 변경 위치만 티켓·Figma 로 특정되면 충분으로 본다. write 도 이런 건 §Cascade 하지 않으므로 prepare 를 부르지 않는다.

### 3. 계획 확인

리포트 요약(티켓 수, 브랜치, base 매핑, PR 개수, §2 에서 보강한 티켓) → AskUserQuestion: 진행 / 취소. 확인 후 질문 없음 — 완료까지 자동.

### 4. 실행 순서

Independent 먼저(순차) → 각 Chain(위상정렬 순).

### 5. 티켓별 처리

각 티켓은 **`/drill:write` 가 정의한 절차**(컨텍스트 로드 → 구현 설계 ↔ 현재 코드 대조 → 작성 → type-check/lint 검증 → SoT 반영)를 그대로 따른다. ship 은 그 바깥만 감싼다:

1. Linear 상태 `In Progress` 전환 (이미면 skip)
2. worktree: `git worktree add ../<repo>-<branch-slug> -b <branch> <base>` → 진입
3. **`/drill:write {ticket}`** — batch 모드(커밋·이어서 질문 생략). 작성·검증·SoT 갱신은 write 책임. 충분성은 §2 에서 이미 보강했으므로 write 가 멈추지 않는다.
4. 커밋 분할 (§6)
5. push: `git push -u origin <branch>`
6. draft PR: `gh pr create --draft --base <base> --title "<conv-commit>" --body "<요약+티켓 링크>"` (또는 `mcp__github__create_pull_request`)
7. PR URL 기록 → 원래 worktree 복귀

실패 시 해당 티켓 중단·기록 후 다음 계속. 단 **chain 내부 중단이면 이후 티켓 skip** (base 미생성).

### 5.5 GitHub stack 등록 (chain 만)

chain 의 PR 이 다 생성되면 GitHub 네이티브 stack 으로 등록한다. base 체이닝만으로는 GitHub 이 stack 으로 인식하지 않는다 — 등록해야 **앞 PR 이 머지될 때 뒤 PR 들이 자동 restack** 되고 리뷰 UI 에 stack 구조가 뜬다.

```bash
gh extension list | grep -q gh-stack   # 없으면 gh extension install github/gh-stack
gh stack link <pr-or-branch> <pr-or-branch> ...   # trunk 에 가까운 순서로
gh stack view                                      # 등록 결과 확인
```

- `link` 는 로컬 stack tracking 없이 **이미 만들어진 브랜치·PR** 을 묶는다 — ship 의 worktree 방식과 그대로 맞는다
- extension 없고 설치도 거절하면 등록을 건너뛰고 최종 리포트에 "stack 미등록 — GitHub PR 화면에서 stack 전환 필요" 로 남긴다 (PR 자체는 정상)
- independent 티켓은 등록 대상 아님
- `gh stack` 은 public preview — 실패해도 ship 을 중단하지 않고 기록만 한다

머지 후 정리는 `gh stack sync`. 등록이 안 됐으면 남은 브랜치를 새 base 위로 순차 rebase 한다.

### 6. 커밋 분할

**PR ≠ 커밋.** 한 커밋 = **하나의 맥락**(함께 바뀌어야 의미가 완성되는 묶음) — 파일·줄 수가 아니라 맥락으로 가른다.

**6.1 1차 그룹핑** — **안쪽(안정) → 바깥쪽(휘발)** 순으로 묶어 그룹별 add + 검증(`write` §4) + Conventional Commit (통과 실패 시 인접 그룹과 병합). 단 한 맥락이 여러 레이어에 걸쳐 한 덩어리면 굳이 쪼개지 않는다.

타입·모델 → 로직(유틸·서비스·use-case) → 경계(포트·어댑터·API) → 표현·어댑터 구현 → 테스트 → 잔여(설정).

**6.2 맥락 단위 재분할** — 1차 결과에서 **한 커밋이 독립된 맥락 여럿을 담으면** 맥락 단위로 쪼갠다. 각 커밋도 type-check/lint 통과 목표, 의존으로 개별 통과 불가하면 병합.

| 신호 | 쪼개는 단위 |
|------|------------|
| 리네임/이동(`R`) + 신규 로직 공존 | 이름 정리 → 로직 변경 |
| 공용 모듈 신규 + 소비처 연결 | 공용 먼저 → 소비처 나중 |
| 한 PR 에 독립 기능 여럿 | 기능(맥락)별 |
| 메시지에 "and/및" 가 필요 | 의미 단위로 |
| 포맷팅 변경 포함 | 별도 chore 로 분리 |

**6.3 실패** — 전체 병합도 실패 → 강제 1커밋 + PR 본문 경고 (질문 없음).

### 7. 최종 리포트

````markdown
# Ship 완료

## PR 목록
| # | Ticket | Branch | Base | PR | Stack |
|---|--------|--------|------|-----|-------|

## Worktree
(경로 목록 — 정리용)

## 보강한 티켓 / 실패 / stack 미등록 / 수집된 [메모] (각각 있을 때만)
- ...
````

## 제약

- 모든 PR `--draft`, 티켓당 1 브랜치 + 1 worktree
- 커밋 분할 완전 자동(질문 없음), 맥락 단위 atomic 지향(§6)
- stacked 체인은 머지 대기 없이 base 에 바로 쌓고, GitHub stack 으로 등록(§5.5)
- 각 티켓 시작 시 Linear `In Progress` 전환
- 부족한 티켓은 §2 에서 먼저 채움 · 자명한 QA 는 건너뜀
- 한국어

## `[메모]` 태그 발화

`[메모]` 로 시작하는 발화 = ship 중단 없는 피드백. 기본은 **세션 완료 후 일괄 반영**(TaskList 축적), 단 지금/방금 끝낸 티켓 PR 안에서 반영 가능하면 즉시. 발견 시 "반영/보류 + 위치(PR#·파일)" 기록, 최종 리포트에 정리.

## 에러

- 티켓 조회 실패 → drill-deps Warnings, 제외
- §2 충분성 미달인데 prepare 강화로도 못 닫음 → 보고 후 제외 (모호성 코드 흡수 금지)
- /drill:write 실패 → 티켓 중단, chain 이면 이후 skip
- type-check/lint 전체 병합도 실패 → 강제 1커밋 + 본문 경고
- `gh pr create` 실패 → 브랜치는 푸시 유지, 실패 기록
- `gh stack link` 실패/미설치 → PR 은 유지, stack 미등록으로 리포트 (ship 중단 X)
- worktree 생성 실패(브랜치명 중복 등) → 티켓 중단

## 관련

- `/drill:prepare` 가 만든 티켓을 batch 처리하는 후속 스킬 — 코드 작성·검증·§Cascade 는 `/drill:write`, ship 은 그 바깥(worktree·커밋분할·push·PR)
- PR 피드백 후 Spec 동기화는 `/drill:review`
