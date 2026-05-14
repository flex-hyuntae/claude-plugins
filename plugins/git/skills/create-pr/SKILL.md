---
name: create-pr
description: 'Conventional Commit 형식(type(scope): subject)의 PR 타이틀과 프로젝트 PR 템플릿 기반 한글 설명을 생성한다. 사용자가 "PR 만들어줘", "create PR", "/git:create-pr", "pull request 생성"을 요청할 때 트리거. 생성 직전 type-check + lint + test 자동 실행(완료 게이트). 자동으로 본인(@me) assignee 지정. 배포 PR(qa/prod)에는 사용하지 않음 — flex-workflow:deploy 사용.'
compatibility: 'gh CLI + GitHub MCP 권장'
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

변경된 파일에서 패키지를 자동 감지하고 type-check + lint + test 를 실행한다. 하나라도 실패하면 PR 생성을 중단하고 사용자에게 수정을 안내한다. 자세한 명령·결과 처리는 [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) 참고.

### 4. Generate PR Title

Conventional Commit 형식 `<type>(<scope>): <subject>` 으로 작성한다.

- **모든 commit** 을 분석해 주된 type 결정 (최신 commit 1개만 보지 말 것)
- **scope** 는 항상 포함 — 주 영향 패키지/도메인 (`remotes-` prefix 제외, 예: `goal`, `auth`, `deps`). cross-cutting이면 `all`
- **subject** 는 한글 명사형/동사형 종결, 72자 이하, 마침표 없음, WHAT만 (구현 디테일은 description으로)

자세한 good/bad 예시와 subject 작성 가이드는 [references/EXAMPLES.md](references/EXAMPLES.md) 참고.

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

Or use the mcp**github**get_me tool to get user information.

### 7. Learnings Summary

PR 생성 직전, 대화를 리뷰해 학습 포인트(Claude가 다르게 접근한 부분 / 사용자가 명시한 학습 포인트)를 사용자 메시지로 전달한다. PR 본문에는 포함하지 않는다. 수집 대상·출력 형식 상세는 [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) 참고.

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
  draft: false,
});
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

Full PR 예시(title + description)는 [references/EXAMPLES.md](references/EXAMPLES.md) 참고.

## Important Notes

- 브랜치의 모든 commit·변경 사항을 분석한다 (최신 commit 1개만 보지 말 것)
- PR 제목·설명 모두 한국어
- base branch는 기본 `develop` — qa/main에는 직접 PR 금지
- 적용 불가한 템플릿 섹션(design/slack)은 비워두거나 제거
- assignee는 항상 `@me` (본인)

## Safety / Error Handling

사전 안전 체크(브랜치·remote 상태·완료 게이트), PR 생성 실패 시 대응, Learnings Summary 처리 등 상세는 [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) 참고.
