---
name: github-pr
description: Conventional Commit 형식의 PR 타이틀과 템플릿 기반 설명을 자동 생성합니다
disable-model-invocation: true
---

# Pull Request

This skill helps create well-formatted Pull Requests with conventional commit titles and organized descriptions based on the project's PR template.

## Workflow

### 1. Check Repository and Branch Status

First, check the current state:

```bash
# Run in parallel
git status
git branch --show-current
git log origin/develop..HEAD --oneline
```

Verify:
- Current branch name
- Base branch (typically `develop`)
- Number of commits ahead of base branch
- Whether there are uncommitted changes (warn if yes)

### 2. Gather Commits and Changes

Analyze all commits in the current branch:

```bash
# Get commit list
git log origin/develop..HEAD --pretty=format:"%h|%s|%b"

# Get overall diff statistics
git diff origin/develop..HEAD --stat

# Get detailed changes for understanding
git diff origin/develop..HEAD
```

### 3. Completion Validation Gate

PR 생성 전 필수 검증을 수행합니다. 하나라도 실패하면 PR 생성을 중단합니다.

**패키지명 자동 감지:**

변경된 파일 경로에서 패키지명을 추출합니다:

```bash
# 변경된 파일 목록에서 패키지 경로 추출
git diff origin/develop..HEAD --name-only | grep -oP 'apps/[^/]+' | sort -u
```

- `apps/remotes-goal` → `@flex-apps/remotes-goal`
- `apps/remotes-evaluation` → `@flex-apps/remotes-evaluation`
- 패키지 감지 불가 시 사용자에게 경고 후 확인

**검증 명령어:**

```bash
# 감지된 각 패키지에 대해 실행
yarn turbo run type-check --filter=@flex-apps/{package-name}
yarn turbo run lint --filter=@flex-apps/{package-name}
yarn turbo run test --filter=@flex-apps/{package-name}
```

**결과 처리:**
- 모두 통과: 다음 단계로 진행
- 실패 항목 있음: 오류 내용 표시 후 PR 생성 중단, 수정 안내
- 테스트가 없는 경우 (`test` 스크립트 미존재): 경고만 표시하고 진행

### 4. Generate PR Title

Use **Conventional Commit** format:

```
<type>(<scope>): <subject>
```

**Critical Rules:**
- **ALWAYS include scope** - it's mandatory, not optional
- Analyze ALL commits in the branch, not just the latest one
- Determine the primary type of change (feat, fix, chore, refactor, etc.)
- Write a concise, imperative subject line in English
- Keep under 72 characters total
- Subject should be lowercase and imperative (add, fix, update, not adds/added)
- No period at the end

**Scope Selection Guide:**
Identify scope from:
1. Main package/application affected (e.g., `remotes-goal`, `payroll`, `user-profile`)
2. Domain area if cross-cutting (e.g., `auth`, `api`, `deps`)
3. Use most specific scope when multiple files changed
4. For monorepo: Use application name without `remotes-` prefix when possible

**Subject Writing Guide:**
- Focus on WHAT changed, not HOW
- Be concise: "use X API" not "change API to use X instead of Y"
- Imperative mood: "add feature" not "adding feature" or "added feature"
- Avoid implementation details in subject (save for description)

**Good Examples:**
- `feat(goal): add excel export functionality`
- `fix(auth): resolve token expiration handling`
- `refactor(user-profile): use search-with-approval API`
- `chore(deps): update react-query to v5`

**Bad Examples:**
- `refactor: 경력/학력/가족 조회 API를 search-with-approval로 변경` (no scope, too long, mixed language, implementation details)
- `Fix bug` (no scope, not specific)
- `feat: Added new feature for users` (no scope, not imperative, capitalized)
- `refactor(remotes-user-profile): change the API endpoint from search to search-with-approval for better approval handling` (too long, too detailed)

### 5. Analyze Changes for PR Description

Read the pull request template:

```bash
# Find PR template in current repo
find . -name "pull_request_template.md" -path "*/.github/*"
```

Analyze changes to fill template sections:

**For standard template sections:**

1. **개요 (Overview)**
   - Summarize the main purpose and goals of this PR
   - What problem does this solve?
   - What feature does this add?

2. **as-is**
   - Describe the current state/behavior before this PR
   - What issues or limitations existed?

3. **to-be**
   - Describe the new state/behavior after this PR
   - How does it improve or change things?

4. **design** (if applicable)
   - Include Figma/design links if changes involve UI
   - Leave blank or remove section if not applicable

5. **slack** (if applicable)
   - Include relevant Slack thread links for context
   - Leave blank or remove section if not applicable

**Analysis approach:**
- Review all modified files and their changes
- Group changes by feature/fix/refactor
- Identify key behavioral changes
- Note any breaking changes or important considerations
- Check for related issues or tickets

### 6. Get Current User Information

```bash
# Get GitHub username for assignment
gh api user --jq '.login'
```

Or use the mcp__github__get_me tool to get user information.

### 7. Learnings Summary

PR 생성 직전, 현재 대화를 리뷰하여 학습 포인트를 **메시지로** 사용자에게 전달합니다. (PR 본문에 넣지 않음)

**수집 대상:**

1. **Claude가 다르게 접근한 부분**: 사용자가 Claude의 코드나 접근 방식을 수정/거부한 경우
   - 예: "이 패턴 대신 X를 사용해" → Claude가 처음 제안한 것과 다른 접근
   - 예: 사용자가 Edit으로 직접 수정한 코드와 Claude가 작성한 코드의 차이

2. **사용자가 명시한 학습 포인트**: "이건 기억해", "이건 배운 점이야", "앞으로는 이렇게 해" 등 명시적 언급

**출력 형식:**

```
## 학습 포인트 정리

### Claude가 다르게 접근한 부분
- [상황]: [Claude의 접근] → [사용자의 수정]
- ...

### 사용자가 명시한 포인트
- [내용]
- ...

> CLAUDE.md에 반영할 내용이 있다면 알려주세요.
```

**규칙:**
- 학습 포인트가 없으면 이 섹션을 건너뜀
- 사용자에게 확인 후, CLAUDE.md에 반영할 내용이 있으면 제안
- PR 본문에는 절대 포함하지 않음

### 8. Create Pull Request

Use the GitHub MCP tool:

```javascript
mcp__github__create_pull_request({
  owner: "<repo-owner>",
  repo: "<repo-name>",
  title: "<conventional-commit-title>",
  head: "<current-branch>",
  base: "develop",
  body: "<filled-pr-template>",
  draft: false
})
```

Then assign to the user:

```bash
# Assign PR to user
gh pr edit <pr-number> --add-assignee @me
```

### 9. Confirm with User

After creating the PR:
- Show the PR URL
- Display the title and description
- Show the assignee
- Confirm creation was successful

### 10. Auto Code Review (Optional)

After PR creation, you may optionally run a code review using the `code-review` plugin if installed:
- `/code-review:code-review` with the newly created PR URL

## PR Description Template Format

The description should follow this structure:

```markdown
# 📝 변경 사항

## 개요
[Brief summary of what this PR does and why]

## as-is
[Current state/behavior before this PR]
- [Specific issue or limitation 1]
- [Specific issue or limitation 2]

## to-be
[New state/behavior after this PR]
- [Improvement or change 1]
- [Improvement or change 2]

# 🔗 같이 보면 좋아요

## design
[Figma or design links, if applicable]

## slack
[Slack thread links for context, if applicable]
```

## Examples

### Example 1: Feature Addition

**Title:**
```
feat(goal): add excel export functionality
```

**Description:**
```markdown
# 📝 변경 사항

## 개요
목표 데이터를 Excel 파일로 내보낼 수 있는 기능을 추가했습니다.

## as-is
- 목표 데이터를 외부로 추출하려면 수동으로 복사/붙여넣기 해야 했습니다.
- 대량의 데이터를 다루기 어려웠습니다.

## to-be
- Excel 내보내기 버튼을 클릭하면 현재 필터된 목표 데이터를 Excel 파일로 다운로드할 수 있습니다.
- 모든 컬럼과 포맷이 유지됩니다.
- 에러 처리 및 성공 알림이 포함되어 있습니다.

# 🔗 같이 보면 좋아요

## design
https://www.figma.com/file/xxxxx

## slack
https://flexhq.slack.com/archives/xxxxx
```

## Important Notes

- Always use conventional commit format for PR title
- Analyze ALL commits and changes in the branch, not just the latest commit
- Fill PR template sections with meaningful content based on actual changes
- Always assign the PR to the user (@me)
- Base branch is typically `develop` unless specified otherwise
- Write descriptions in Korean (한국어) for Flex project
- Remove or leave blank template sections that don't apply (design, slack)
- Check for uncommitted changes and warn user before creating PR
- Ensure the branch is pushed to remote before creating PR

## Error Handling

If PR creation fails:
- Show the error message to the user
- Check if branch is pushed to remote (if not, ask user to push)
- Check if PR already exists between these branches
- Verify repository permissions
- Suggest potential fixes

If branch is not pushed:
```bash
# Offer to push the branch
git push -u origin <current-branch>
```

## Safety Checks

Before creating PR:
- Check that current branch is not `develop`, `qa`, or `main`
- Verify there are commits ahead of base branch
- Warn if there are uncommitted changes
- Check if branch exists on remote (push if needed)
- Ensure user is authenticated with GitHub
