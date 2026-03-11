---
name: git-rebase-stack
description: Stacked PR의 base branch merge 후 나머지 branch들을 순차 rebase합니다
disable-model-invocation: true
---

# Restack

이 skill은 stacked PR에서 base branch가 merge된 후 나머지 branch들을 순차적으로 rebase하고 force push합니다.

## 사용자 입력 형식

```
restack <base-branch> <branch1> <branch2> ...
```

**Full chain을 입력합니다** — merge된 branch도 포함합니다.

예: `restack develop feat/A feat/B feat/C` → A가 이미 merge되었더라도 chain에 포함하여, B와 C를 정확히 rebase

## Workflow

### 1. 상태 확인

먼저 저장소의 현재 상태를 확인합니다:

```bash
# Run in parallel
git status --porcelain
git fetch origin
git worktree list
```

확인 항목:

- **Working tree가 clean한지 확인** — 변경 사항이 있으면 중단하고 사용자에게 알림
- **모든 대상 branch가 존재하는지 확인** — `git branch --list <branch>` 로 각 branch 존재 여부 확인
- **Worktree에서 checkout된 branch가 없는지 확인** — `git worktree list` 출력에서 대상 branch가 없어야 함

상태 확인 실패 시:

- Working tree가 dirty하면: "커밋하지 않은 변경 사항이 있습니다. 먼저 commit하거나 stash해주세요." 안내 후 종료
- Branch가 존재하지 않으면: 해당 branch 이름을 알려주고 종료
- Worktree에서 checkout되어 있으면: "해당 branch가 worktree에서 사용 중입니다." 안내 후 종료

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

**핵심 알고리즘 (`--onto` + old tip 기반):**

`current_target`을 base-branch로 초기화하고, chain의 각 branch를 순서대로 처리합니다.

```
current_target = <base-branch>

for each bi in [branch1, branch2, ...]:
  if bi is merged:
    skip (current_target 변경 없음)
  else:
    old_parent = OLD tip of previous branch in chain
                 (첫 번째 unmerged branch이고 이전이 모두 merged이면:
                  git merge-base <bi> <base-branch>)
    git rebase --onto $current_target $old_parent bi
    current_target = bi
```

**구체적 실행 예시** (`develop → a → b → c`, a가 squash merge됨):

```bash
# 사전 저장된 old tips
OLD_A=...  OLD_B=...  OLD_C=...

# a: merged → skip, current_target = develop

# b: unmerged, 이전 branch = a (merged)
#    old_parent = OLD_A (a의 rebase 전 tip)
git rebase --onto develop $OLD_A b
# → a의 커밋 제외, b 자체 커밋만 replay
# current_target = b

# c: unmerged, 이전 branch = b
#    old_parent = OLD_B
git rebase --onto b $OLD_B c
# current_target = c
```

**`old_parent` 결정 규칙:**

| 상황 | old_parent |
|------|-----------|
| 이전 branch가 chain에 존재 (merged/unmerged 무관) | 이전 branch의 OLD tip |
| chain의 첫 번째 branch이면서 unmerged | `git merge-base <branch> <base-branch>` |

각 rebase 완료 후 결과를 표시합니다:

```
✅ feat/B: develop 위로 rebase 완료 (abc1234 → def5678)
```

### 5. 충돌 처리

Rebase 중 충돌이 발생하면:

1. **즉시 멈추고** 충돌 파일 목록을 표시합니다:

```bash
git diff --name-only --diff-filter=U
```

2. 사용자에게 안내합니다:

```
⚠️ feat/B를 rebase하는 중 충돌이 발생했습니다.

충돌 파일:
- src/components/UserList.tsx
- src/hooks/useUsers.ts

충돌을 해결한 후 알려주세요.
```

3. `AskUserQuestion`으로 **"충돌을 해결하셨나요? (해결완료 / 중단)"** 질문합니다.

4. 사용자가 "해결했다"/"해결완료"라고 답하면:

```bash
git add .
git rebase --continue
```

- 성공하면 다음 branch로 계속 진행
- 또 충돌이 나면 다시 1번으로 돌아감

5. 사용자가 "중단"이라고 답하면:

```bash
git rebase --abort
```

중단 사유를 표시하고 skill을 종료합니다.

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

모든 작업 완료 후 최종 결과를 보고합니다:

```
🎉 Restack 완료!

📊 결과:
  ✅ feat/B: develop 위로 rebase 완료 + push 완료
  ✅ feat/C: feat/B 위로 rebase 완료 + push 완료

📐 최종 Stack 구조:
  develop
  └── feat/B (3 commits)
      └── feat/C (2 commits)
```

## 예시

### 예시 1: 기본 사용 (merged branch 없음)

```
restack develop feat/auth-api feat/auth-ui feat/auth-tests
```

결과:
- `feat/auth-api`를 `develop` 위로 rebase (`--onto develop $(merge-base) feat/auth-api`)
- `feat/auth-ui`를 rebased `feat/auth-api` 위로 rebase (`--onto feat/auth-api $OLD_API feat/auth-ui`)
- `feat/auth-tests`를 rebased `feat/auth-ui` 위로 rebase (`--onto feat/auth-ui $OLD_UI feat/auth-tests`)

### 예시 2: 첫 번째 branch가 squash merge된 경우

`develop → A → B → C` 에서 A가 develop으로 squash merge된 후:

```
restack develop feat/A feat/B feat/C
```

결과:
- `feat/A`: merged → skip
- `feat/B`: `git rebase --onto develop $OLD_A feat/B` (A의 커밋 제외, B 자체 커밋만 replay)
- `feat/C`: `git rebase --onto feat/B $OLD_B feat/C`

### 예시 3: 중간 branch가 merge된 경우

`develop → A → B → C → D` 에서 A, B가 순차 merge된 후:

```
restack develop feat/A feat/B feat/C feat/D
```

결과:
- `feat/A`: merged → skip
- `feat/B`: merged → skip
- `feat/C`: `git rebase --onto develop $OLD_B feat/C` (current_target은 develop, old_parent는 B의 old tip)
- `feat/D`: `git rebase --onto feat/C $OLD_C feat/D`

## 중요 사항

- **Full chain 입력**: merged branch도 포함하여 정확한 old tip 기반 rebase를 보장합니다
- **Working tree는 반드시 clean 상태**여야 합니다
- **Protected branch (develop, qa, main)에는 절대 force push하지 않습니다**
- `--force-with-lease`를 사용하여 다른 사람의 push를 덮어쓰지 않도록 합니다
- 충돌 발생 시 사용자에게 해결을 맡기고, 해결 후 계속 진행합니다
- 모든 주요 단계에서 사용자 확인을 받습니다 (계획, push)
- Rebase 전 모든 branch의 tip을 미리 저장하여 `--onto`의 upstream으로 사용합니다
- Squash merge된 branch는 자동 감지 불가 — 사용자 확인을 통해 판정합니다

## 오류 처리

- **git fetch 실패**: 네트워크 연결 확인 안내
- **Branch 없음**: 해당 branch 이름 표시 후 종료
- **Worktree 충돌**: worktree에서 checkout된 branch 안내 후 종료
- **Rebase 충돌**: 충돌 파일 표시 후 사용자에게 해결 요청
- **Push 실패**: 오류 메시지 표시 후 재시도 여부 확인
