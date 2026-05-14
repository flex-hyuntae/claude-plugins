---
name: rebase-stack
description: 'Stacked PR에서 base branch가 merge된 후 나머지 branch들을 순차 rebase하고 force-with-lease로 push한다. 사용자가 "restack", "/git:rebase-stack", "스택 정리", "rebase stack", "base가 merge됐어 나머지 rebase해줘"를 요청할 때 트리거. Full chain 입력 필수(merge된 branch 포함). Worktree에서 사용 중인 branch나 working tree dirty 상태면 중단. 보호 브랜치(develop/qa/main)에는 push 안 함.'
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

3가지 대표 시나리오(merged 없음 / 첫 번째 squash merge / 중간 branch merge)는 [references/SCENARIOS.md](references/SCENARIOS.md) 참고.

## 중요 사항

- Full chain 입력 (merged branch 포함) — 정확한 old tip 기반 rebase의 전제
- Working tree clean 상태 필수
- 보호 브랜치(develop/qa/main)에는 force push 금지
- `--force-with-lease` 사용 (다른 사람의 push 덮어쓰기 방지)
- 모든 주요 단계(계획·push)에서 사용자 확인
- Squash merge는 자동 감지 불가 — 사용자 확인으로 판정

## 오류 처리

- git fetch 실패 → 네트워크 확인 안내
- Branch 없음 → 해당 이름 표시 후 종료
- Worktree에서 사용 중 → 해당 branch 안내 후 종료
- Rebase 충돌 → 충돌 파일 표시 후 사용자에게 해결 요청 (위 Step 5)
- Push 실패 → 오류 메시지 표시 후 재시도 여부 확인
