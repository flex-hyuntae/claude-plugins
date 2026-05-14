# Restack Scenarios & Algorithm

## 핵심 알고리즘 (`--onto` + old tip)

`current_target`을 base-branch로 초기화하고, chain의 각 branch를 순서대로 처리한다.

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

### `old_parent` 결정 규칙

| 상황 | old_parent |
|------|-----------|
| 이전 branch가 chain에 존재 (merged/unmerged 무관) | 이전 branch의 OLD tip |
| chain의 첫 번째 branch이면서 unmerged | `git merge-base <branch> <base-branch>` |

## 시나리오 예시

### 예시 1: 기본 사용 (merged branch 없음)

```
restack develop feat/auth-api feat/auth-ui feat/auth-tests
```

실행:
- `feat/auth-api` → `git rebase --onto develop $(git merge-base feat/auth-api develop) feat/auth-api`
- `feat/auth-ui` → `git rebase --onto feat/auth-api $OLD_API feat/auth-ui`
- `feat/auth-tests` → `git rebase --onto feat/auth-ui $OLD_UI feat/auth-tests`

### 예시 2: 첫 번째 branch가 squash merge된 경우

`develop → A → B → C`, A가 develop으로 squash merge된 후:

```
restack develop feat/A feat/B feat/C
```

실행:
- `feat/A`: merged → skip
- `feat/B`: `git rebase --onto develop $OLD_A feat/B` (A의 커밋 제외, B 자체 커밋만 replay)
- `feat/C`: `git rebase --onto feat/B $OLD_B feat/C`

### 예시 3: 중간 branch가 merge된 경우

`develop → A → B → C → D`, A·B가 순차 merge된 후:

```
restack develop feat/A feat/B feat/C feat/D
```

실행:
- `feat/A`: merged → skip
- `feat/B`: merged → skip
- `feat/C`: `git rebase --onto develop $OLD_B feat/C` (current_target은 develop, old_parent는 B의 old tip)
- `feat/D`: `git rebase --onto feat/C $OLD_C feat/D`

## 구체적 실행 예시 (develop → a → b → c, a가 squash merge됨)

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

## 충돌 처리 상세 플로우

Rebase 중 충돌이 발생하면:

1. **즉시 멈추고** 충돌 파일 목록을 표시:

```bash
git diff --name-only --diff-filter=U
```

2. 사용자에게 안내:

```
⚠️ feat/B를 rebase하는 중 충돌이 발생했습니다.

충돌 파일:
- src/components/UserList.tsx
- src/hooks/useUsers.ts

충돌을 해결한 후 알려주세요.
```

3. `AskUserQuestion`으로 "충돌을 해결하셨나요? (해결완료 / 중단)" 질문.

4. "해결완료" 답변 시:

```bash
git add .
git rebase --continue
```

- 성공 → 다음 branch로 진행
- 또 충돌 → 1번으로 돌아감

5. "중단" 답변 시:

```bash
git rebase --abort
```

중단 사유 표시 후 종료.

## Squash merge 자동 감지 불가 케이스

`git merge-base --is-ancestor <branch> <base-branch>` 검사가 실패하지만 실제로는 squash merge된 경우. rebase 계획 단계에서 `AskUserQuestion`으로 확인:

```
❓ feat/A 브랜치가 develop에 이미 merge되었나요?
   (squash merge는 자동 감지가 불가합니다)
   [예 / 아니오]
```

## Push 결과 표시 형식

```
🚀 Force push 준비:

다음 branch들을 force push합니다:
1. feat/B → origin/feat/B
2. feat/C → origin/feat/C

각 branch를 force push하시겠습니까?
```

확인 후:

```bash
git push --force-with-lease origin <branch1>
git push --force-with-lease origin <branch2>
```

```
✅ feat/B → origin/feat/B push 완료
✅ feat/C → origin/feat/C push 완료
```

## 최종 결과 보고 형식

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
