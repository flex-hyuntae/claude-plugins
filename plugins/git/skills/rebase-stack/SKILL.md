---
name: rebase-stack
description: 'Stacked PR에서 base branch가 merge된 후 나머지 branch들을 rebase하고 force-with-lease로 push한다. GitHub 네이티브 stack(gh stack)이 있으면 cascading rebase를 위임하고, 없으면 수동 순차 rebase로 폴백. 사용자가 "restack", "/git:rebase-stack", "스택 정리", "rebase stack", "base가 merge됐어 나머지 rebase해줘"를 요청할 때 트리거. 수동 경로는 full chain 입력 필수(merge된 branch 포함). Worktree에서 사용 중인 branch나 working tree dirty 상태면 중단. 보호 브랜치(develop/qa/main)에는 push 안 함.'
compatibility: 'gh CLI 2.90+ · gh stack extension 있으면 자동 위임, 없으면 수동 폴백'
disable-model-invocation: true
---

# Restack

Stacked PR 에서 앞 branch 가 merge된 후 나머지를 rebase + force push 한다.

## 경로 선택 (Phase 0)

```bash
gh extension list | grep -q gh-stack && gh stack view 2>/dev/null
```

| 상태 | 경로 |
|------|------|
| extension 있음 + 현재 브랜치가 stack 소속 | **A. gh stack 위임** (§A) |
| extension 있음 + stack 미등록 | 브랜치들을 `gh stack link` 로 등록할지 AskUserQuestion → 등록하면 A, 거절하면 B |
| extension 없음 | 설치 안내(`gh extension install github/gh-stack`) + AskUserQuestion → 설치하면 A, 거절하면 B |

`gh stack` 은 public preview 다. 동작이 예상과 다르면 B 로 폴백하고 사유를 보고한다.

---

## A. gh stack 위임

`gh stack rebase` 는 remote 를 pull 하고 stack 전체에 cascading rebase 를 수행한다. **앞 PR 이 merge 됐으면 자동으로 `--onto` 모드로 전환**해 올바른 merge target 위에 replay 하므로, §B 가 손으로 하는 squash merge 판정·`old_parent` 계산이 불필요하다.

```bash
gh stack view              # 현재 구조·PR 상태 확인 (변경 전)
gh stack sync              # fetch + rebase + push + PR 상태 동기화 (rebase 발생 시 --force-with-lease)
gh stack view              # 결과 확인
```

- `sync` 는 push 까지 한다 — 실행 전 구조를 보여주고 **AskUserQuestion 으로 확인**받는다
- push 없이 rebase 만 원하면 `gh stack rebase` 후 §6 으로 push
- 충돌 발생 시 §5 와 동일하게 처리 (`gh stack rebase` 는 표준 rebase 를 쓴다)
- 구조 자체를 바꿔야 하면(순서 변경·중간 제거) `gh stack modify` — clean working tree + linear history 필요

보호 브랜치 규칙(§6)은 A 에서도 유효하다. trunk 가 `develop`/`qa`/`main` 인 것은 정상이며 stack 은 trunk 에 push 하지 않는다.

---

## B. 수동 폴백

### 사용자 입력 형식

```
restack <base-branch> <branch1> <branch2> ...
```

**Full chain을 입력합니다** — merge된 branch도 포함합니다.

예: `restack develop feat/A feat/B feat/C` → A가 이미 merge되었더라도 chain에 포함하여, B와 C를 정확히 rebase

### 1. 상태 확인

```bash
# Run in parallel
git status --porcelain
git fetch origin
git worktree list
```

다음 중 하나라도 어긋나면 사유를 안내하고 중단한다:

- Working tree dirty (먼저 commit/stash 필요)
- 대상 branch 미존재 (`git branch --list <branch>`)
- 대상 branch가 worktree에서 checkout 중

### 2. Old Tip 저장 및 Merged Branch 감지

**모든 branch의 현재 tip을 rebase 시작 전에 미리 저장합니다:**

```bash
OLD_BRANCH1=$(git rev-parse <branch1>)
OLD_BRANCH2=$(git rev-parse <branch2>)
OLD_BRANCH3=$(git rev-parse <branch3>)
# ...
```

**각 branch가 base에 이미 merge되었는지 감지합니다:**

```bash
# regular merge / fast-forward 감지
git merge-base --is-ancestor <branch> <base-branch>
```

- 성공(exit 0) → merged로 판정, rebase에서 skip
- 실패(exit 1) → merged 아님, rebase 대상

**Squash merge 대응**: `--is-ancestor` 검사가 실패하지만 실제로는 merge된 경우가 있습니다 (squash merge). 이 경우 rebase 계획 단계에서 사용자에게 `AskUserQuestion`으로 확인합니다:

```
❓ feat/A 브랜치가 develop에 이미 merge되었나요?
   (squash merge는 자동 감지가 불가합니다)
   [예 / 아니오]
```

### 3. Rebase 계획 수립 및 확인

merged/unmerged 판정 결과를 기반으로 rebase 대상 branch와 commit 수를 파악합니다:

```bash
# unmerged branch만 대상. 이전 branch 대비 commit 수
git log --oneline <prev-branch>..<branch>
```

계획을 사용자에게 보여줍니다:

```
📋 Rebase 계획:

  ⏭️ feat/A: merged → skip
  1. feat/B (3 commits) → develop 위로 rebase (--onto develop $OLD_A)
  2. feat/C (2 commits) → rebased feat/B 위로 rebase (--onto feat/B $OLD_B)

계속 진행하시겠습니까?
```

`AskUserQuestion`으로 확인을 받습니다. 사용자가 거절하면 종료합니다.

### 4. 순차 Rebase 실행

`current_target`을 base-branch로 초기화하고 chain을 순서대로 돌면서 unmerged branch만 `git rebase --onto $current_target $old_parent <branch>` 로 옮긴다. `old_parent`는 이전 branch의 OLD tip(merged 무관). 알고리즘 의사코드·구체 실행 예시·old_parent 결정 표는 [references/SCENARIOS.md](references/SCENARIOS.md) 참고.

각 rebase 완료 후 `✅ feat/B: develop 위로 rebase 완료 (abc1234 → def5678)` 형식으로 표시.

### 5. 충돌 처리

Rebase 중 충돌 발생 시 즉시 멈추고 충돌 파일을 보여준 뒤 `AskUserQuestion` 으로 "해결완료 / 중단" 질문. "해결완료" → `git add . && git rebase --continue`, "중단" → `git rebase --abort` 후 종료. 안내 메시지 포맷·반복 충돌 대응 상세는 [references/SCENARIOS.md](references/SCENARIOS.md) 참고.

### 6. Force Push

모든 rebase가 완료된 후 각 branch를 force push합니다.

**안전 규칙:**

- `--force-with-lease` 사용 (안전한 force push)
- **`develop`, `qa`, `main` branch로는 절대 push 금지** — 이 branch가 대상에 포함되어 있으면 건너뛰고 경고
- 각 branch push 전 `AskUserQuestion`으로 확인

```
🚀 Force push 준비:

다음 branch들을 force push합니다:
1. feat/B → origin/feat/B
2. feat/C → origin/feat/C

각 branch를 force push하시겠습니까?
```

사용자가 확인하면:

```bash
git push --force-with-lease origin <branch1>
git push --force-with-lease origin <branch2>
```

각 push 결과를 표시합니다:

```
✅ feat/B → origin/feat/B push 완료
✅ feat/C → origin/feat/C push 완료
```

### 7. 결과 보고

각 branch의 rebase+push 결과와 최종 stack 구조를 보고한다. **gh stack extension 미설치로 B 를 탄 경우** 마지막에 한 줄 안내: 설치하면(`gh extension install github/gh-stack`) 다음부터 §A 로 squash merge 판정 없이 처리된다.

## 예시

3가지 대표 시나리오(merged 없음 / 첫 번째 squash merge / 중간 branch merge)는 [references/SCENARIOS.md](references/SCENARIOS.md) 참고. §A 로 처리되면 이 시나리오 구분 자체가 필요 없다 — `gh stack rebase` 가 merge 여부를 스스로 판정한다.
