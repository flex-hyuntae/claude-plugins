---
name: commit
description: Conventional Commits 형식의 커밋 메시지를 생성합니다
disable-model-invocation: true
---

# Git Commit

This skill helps create well-formatted git commits following Conventional Commits specification.

## Workflow

### 1. Check Repository Status

First, check the current state of the repository:

```bash
# Run in parallel
git status
git diff --cached --name-status
git diff --name-status
```

### 2. Determine Files to Commit

**If there are staged files:**
- Use only staged files (do not run `git add`)

**If no files are staged but there are modified files:**
- Show the list of modified files to the user
- Ask which files they want to commit
- Stage only the selected files

**If no changes at all:**
- Inform the user there are no changes to commit
- Exit gracefully

### 3. Analyze Changes

For the files to be committed:

```bash
# View the actual changes
git diff --cached

# If needed, read specific files to understand context
```

Analyze:
- What type of change is this? (feat, fix, chore, docs, refactor, style, test, build, ci, perf, revert)
- **REQUIRED**: Determine the scope based on file paths:
  - Look at the directory structure (e.g., `remotes-goal` → `goal`, `packages/core-*-hooks` → `core-hooks`)
  - Use the primary domain or feature name affected
  - Use `all` only if multiple distinct domains are affected
- What is the purpose and impact of the change?

### 4. Generate Commit Message

Follow this format:

```
<type>(<scope>): <subject>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Type selection rules:**
- `feat`: New feature or functionality
- `fix`: Bug fix
- `chore`: Maintenance tasks (dependencies, configs, build scripts)
- `refactor`: Code restructuring without changing behavior
- `docs`: Documentation changes
- `style`: Code formatting, whitespace, missing semicolons
- `test`: Adding or updating tests
- `build`: Build system or external dependencies
- `ci`: CI/CD configuration changes
- `perf`: Performance improvements
- `revert`: Reverting a previous commit

**Scope guidelines:**
- **REQUIRED**: Scope must always be included (e.g., `goal`, `evaluation`, `review`, `user`, `auth`)
- Use the domain or feature name based on the files being changed
- Use `all` for changes affecting multiple domains
- Never omit the scope - every commit must have one

**Subject line:**
- **한글로 작성** (예: "목표 데이터 엑셀 내보내기 기능 추가")
- 간결한 명사형/동사형 종결 ("추가", "수정", "변경")
- No period at the end
- Keep under 50 characters if possible
- Be specific and descriptive

**Body (optional):**
- Add only if the change needs explanation beyond the subject
- Explain WHY, not WHAT (the diff shows what)
- Wrap at 72 characters

### 5. Create the Commit

IMPORTANT Git Safety Protocol:
- NEVER update git config
- NEVER run destructive commands (push --force, hard reset, etc.) unless explicitly requested
- NEVER skip hooks (--no-verify, --no-gpg-sign) unless explicitly requested
- NEVER use `git commit --amend` (create new commits instead)
- DO NOT push to remote unless explicitly requested

```bash
# Stage files if needed (only if user selected specific files)
git add <selected-files>

# Create commit using HEREDOC for proper formatting
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Verify the commit was created
git log -1 --oneline
```

### 6. Confirm with User

After creating the commit:
- Show the commit message that was created
- Show the commit hash and summary
- Confirm the commit was successful

## Examples

### Example 1: Feature Addition

```
feat(goal): 목표 데이터 엑셀 내보내기 기능 추가

목표 데이터를 Excel 파일로 내보내는 버튼과 API 연동을 추가.
에러 처리 및 성공 알림 포함.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 2: Bug Fix

```
fix(auth): 토큰 만료 처리 오류 수정

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 3: Chore

```
chore(deps): react-query v5.0.0 업데이트

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 4: Refactoring

```
refactor(review): 리뷰 코멘트 로직을 커스텀 훅으로 분리

복잡한 코멘트 처리 로직을 useReviewComments 훅으로 분리하여
테스트 용이성과 재사용성 개선.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### BAD Examples (Missing Scope)

```
# WRONG - Missing scope
refactor: 리뷰 코멘트 로직을 커스텀 훅으로 분리

# WRONG - Missing scope
fix: 토큰 만료 처리 오류 수정

# CORRECT - With scope
refactor(review): 리뷰 코멘트 로직을 커스텀 훅으로 분리
fix(auth): 토큰 만료 처리 오류 수정
```

## Important Notes

- **CRITICAL**: Scope is ALWAYS required - never create commits without scope
- Always follow the Conventional Commits format strictly
- Analyze the actual code changes, don't just rely on file names
- Be concise but descriptive in commit messages
- Never commit files that likely contain secrets (.env, credentials.json, etc.)
- If you see potential secrets, warn the user before committing
- Keep commit scope focused - suggest splitting if changes are too diverse
- Always include the Co-Authored-By line to indicate Claude collaboration

## Error Handling

If commit fails:
- Show the error message to the user
- Suggest potential fixes (e.g., pre-commit hook failures, merge conflicts)
- Do NOT use `--amend` or `--no-verify` unless explicitly requested
- Create a NEW commit after fixing issues
