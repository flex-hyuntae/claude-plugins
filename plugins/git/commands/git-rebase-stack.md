# Restack Skill

이 skill은 stacked PR에서 base branch가 merge된 후 나머지 branch들을 순차적으로 rebase하고 force push합니다.

## 사용자 입력 형식

```
restack <base-branch> <branch1> <branch2> ...
```

예: `restack develop feat/B feat/C` → develop 위로 B를 rebase, rebased B 위로 C를 rebase

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

### 2. Rebase 계획 수립 및 확인

각 branch에 대해 commit 수를 파악합니다:

```bash
# 첫 번째 branch: base-branch 대비 commit 수
git log --oneline <base-branch>..<branch1>

# 두 번째 branch: 이전 branch 대비 commit 수
git log --oneline <branch1>..<branch2>

# ...이후 branch도 동일
```

계획을 사용자에게 보여줍니다:

```
📋 Rebase 계획:

1. feat/B (3 commits) → develop 위로 rebase
2. feat/C (2 commits) → rebased feat/B 위로 rebase

계속 진행하시겠습니까?
```

`AskUserQuestion`으로 확인을 받습니다. 사용자가 거절하면 종료합니다.

### 3. 순차 Rebase 실행

**핵심 알고리즘 (merge-base 기반):**

각 branch를 순서대로 rebase합니다. 다음 branch를 rebase할 때 이전 branch의 **rebase 전 tip**을 old-parent로 사용합니다.

```bash
# === 첫 번째 branch: base-branch 위로 rebase ===
OLD_BRANCH1=$(git rev-parse <branch1>)
MERGE_BASE_1=$(git merge-base <branch1> <base-branch>)
git rebase --onto <base-branch> $MERGE_BASE_1 <branch1>

# === 두 번째 branch: rebased branch1 위로 rebase ===
# OLD_BRANCH1은 rebase 전 branch1의 tip (이미 저장됨)
git rebase --onto <branch1> $OLD_BRANCH1 <branch2>

# === 세 번째 branch: rebased branch2 위로 rebase ===
# 패턴 동일: 이전 branch의 rebase 전 tip을 old-parent로 사용
OLD_BRANCH2=$(...)  # rebase 전에 미리 저장
git rebase --onto <branch2> $OLD_BRANCH2 <branch3>
```

**중요**: 모든 branch의 rebase 전 tip을 **rebase 시작 전에 미리 저장**해야 합니다.

```bash
# 모든 branch의 현재 tip을 미리 저장
OLD_BRANCH1=$(git rev-parse <branch1>)
OLD_BRANCH2=$(git rev-parse <branch2>)
OLD_BRANCH3=$(git rev-parse <branch3>)
# ...
```

각 rebase 완료 후 결과를 표시합니다:

```
✅ feat/B: develop 위로 rebase 완료 (abc1234 → def5678)
```

### 4. 충돌 처리

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

### 5. Force Push

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

### 6. 결과 보고

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

### 예시 1: 기본 사용

```
restack develop feat/auth-api feat/auth-ui feat/auth-tests
```

결과:
- `feat/auth-api`를 `develop` 위로 rebase
- `feat/auth-ui`를 rebased `feat/auth-api` 위로 rebase
- `feat/auth-tests`를 rebased `feat/auth-ui` 위로 rebase

### 예시 2: 중간 branch가 merge된 경우

`develop → A → B → C` 에서 A가 develop으로 merge된 후:

```
restack develop feat/B feat/C
```

결과:
- `feat/B`를 `develop` (A가 merge된 상태) 위로 rebase
- `feat/C`를 rebased `feat/B` 위로 rebase

## 중요 사항

- **Working tree는 반드시 clean 상태**여야 합니다
- **Protected branch (develop, qa, main)에는 절대 force push하지 않습니다**
- `--force-with-lease`를 사용하여 다른 사람의 push를 덮어쓰지 않도록 합니다
- 충돌 발생 시 사용자에게 해결을 맡기고, 해결 후 계속 진행합니다
- 모든 주요 단계에서 사용자 확인을 받습니다 (계획, push)
- Rebase 전 모든 branch의 tip을 미리 저장하여 정확한 rebase를 보장합니다

## 오류 처리

- **git fetch 실패**: 네트워크 연결 확인 안내
- **Branch 없음**: 해당 branch 이름 표시 후 종료
- **Worktree 충돌**: worktree에서 checkout된 branch 안내 후 종료
- **Rebase 충돌**: 충돌 파일 표시 후 사용자에게 해결 요청
- **Push 실패**: 오류 메시지 표시 후 재시도 여부 확인
