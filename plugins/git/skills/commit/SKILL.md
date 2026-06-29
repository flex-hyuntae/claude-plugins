---
name: commit
description: 'Conventional Commits 형식(type(scope): subject)으로 커밋 메시지를 생성하고 staged 파일만 커밋한다. 사용자가 "commit", "커밋", "/git:commit", "커밋 만들어줘", "변경사항 커밋"을 요청할 때 트리거. scope는 항상 포함 — 파일 경로 기반 도메인을 추출한다(PR 검색·changelog·코드 오너 매핑이 scope 기반이라 누락되면 자동화가 깨진다). secrets 의심 파일(.env 등)은 사전 경고, amend·no-verify는 명시 요청 없으면 사용하지 않음. subject는 한글 명사형/동사형.'
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

`git diff --cached` 로 실제 변경을 분석한다:
- Type: feat, fix, chore, docs, refactor, style, test, build, ci, perf, revert
- Scope: 파일 경로에서 도메인 추출 (예: `apps/remotes-goal/...` → `goal`, `packages/core-*-hooks/...` → `core-hooks`). 여러 도메인이 섞이면 `all`. 자세한 추출 패턴은 [references/EXAMPLES.md](references/EXAMPLES.md)
- Purpose: 이 변경의 목적과 영향

### 4. Generate Commit Message

Follow this format:

```
<type>(<scope>): <subject>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Subject line:**
- **한글로 작성** (예: "목표 데이터 엑셀 내보내기 기능 추가")
- 간결한 명사형/동사형 종결 ("추가", "수정", "변경"), 마침표 없음

**Body (optional):** 제목만으로 부족할 때만, WHAT이 아닌 WHY를 설명.

### 5. Create the Commit

Git Safety: 명시 요청 없이는 config 변경·force/hard reset·hook skip(--no-verify)·`--amend`·remote push 금지 (새 커밋 생성).

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

## Examples

자세한 good/bad 예시와 scope 추출 패턴 표는 [references/EXAMPLES.md](references/EXAMPLES.md) 참고.

## Important Notes

- secrets 의심 파일(.env, credentials.json 등)은 커밋 전 사용자에게 경고
- 한 커밋에 여러 도메인이 섞이면 분리 제안

## Error Handling

커밋 실패 시 에러와 가능한 원인(pre-commit hook 실패, merge conflict 등)을 사용자에게 안내. hook 실패 시에도 `--amend`/`--no-verify`로 우회하지 않는다 (새 커밋이 안전).
