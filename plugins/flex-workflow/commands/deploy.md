---
name: deploy
description: QA/Prod 배포 PR을 커밋 요약과 함께 자동 생성합니다
---

# Deploy

This skill creates deployment Pull Requests for QA and Production stages with organized commit summaries.

## Workflow

### 1. Parse User Input

When user types `deploy {qa|prod}`, extract the stage:
- `deploy qa` → QA deployment
- `deploy prod` → Production deployment

### 2. Calculate Deploy Date

```bash
# For QA: today + 2 days
# For Prod: today

# Get current date
CURRENT_DATE=$(date +%Y-%m-%d)

# For QA, add 2 days
QA_DATE=$(date -v+2d +%Y-%m-%d)

# Format: YYYY-MM-DD
# Ensure single-digit dates have leading zero (already handled by date format)
```

**Date formatting for PR title:**
- Extract year, month, date
- Add leading zero if month or date is single digit
- Format: `v2.{year}-{month}-{date}.0`
- Example: `v2.2026-01-15.0`

### 3. Sync Branches with Remote

ALWAYS sync both base and head branches before creating PR:

```bash
# For QA deployment
git fetch origin
git checkout qa
git pull origin qa
git checkout develop
git pull origin develop

# For Prod deployment
git fetch origin
git checkout main
git pull origin main
git checkout qa
git pull origin qa
```

### 4. Get Commit History

**For QA (`develop` → `qa`):**
```bash
git log qa..develop --format="%H|%s|%an" --no-merges
```

**For Prod (`qa` → `main`):**
```bash
git log main..qa --format="%H|%s|%an" --no-merges
```

Output format: `{commit_hash}|{commit_subject}|{author_name}`

### 5. Parse Commits and Map to PRs

For each commit:

1. **Parse commit message:**
   ```
   fix(objective): fix issue with objective (#4156)
   ```
   - Type: `fix`
   - Domain: `objective`
   - Message: `fix issue with objective`
   - PR number: `4156` (if present in commit message)

2. **Extract PR number:**
   - Look for `(#XXXX)` pattern in commit subject
   - If not found, search GitHub using commit message

3. **Build commit data structure:**
   ```json
   {
     "hash": "abc123",
     "type": "fix",
     "domain": "objective",
     "message": "fix issue with objective",
     "pr_number": "4156",
     "author": "John Doe"
   }
   ```

### 6. Generate PR Body

Create a markdown file with three sections:

#### Section 1: Domains
Group commits by domain (scope):

```markdown
# Domains
## objective
- [fix: fix issue with objective](https://github.com/{owner}/{repo}/pull/4156)
- [feat: add new objective feature](https://github.com/{owner}/{repo}/pull/4157)
## user
- [fix: fix user authentication bug](https://github.com/{owner}/{repo}/pull/4158)
```

#### Section 2: Orders
List all commits in chronological order:

```markdown
# Orders
- [fix: fix issue with objective](https://github.com/{owner}/{repo}/pull/4156)
- [feat: add new objective feature](https://github.com/{owner}/{repo}/pull/4157)
- [fix: fix user authentication bug](https://github.com/{owner}/{repo}/pull/4158)
```

#### Section 3: Authors
Group commits by author:

```markdown
# Authors
## John Doe
- [fix: fix issue with objective](https://github.com/{owner}/{repo}/pull/4156)
- [feat: add new objective feature](https://github.com/{owner}/{repo}/pull/4157)
## Jane Smith
- [fix: fix user authentication bug](https://github.com/{owner}/{repo}/pull/4158)
```

### 7. Create Deployment Summary File

```bash
# Create temporary file in project root
cat > deployment-summary.md <<'EOF'
# Domains
...

# Orders
...

# Authors
...
EOF
```

### 8. Create Pull Request

**IMPORTANT: PR Body Creation**

Use one of these correct methods:

**Method 1: Store content in variable first**
```bash
BODY_CONTENT=$(cat deployment-summary.md)
gh pr create --title "..." --base qa --head develop --assignee @me --body "$BODY_CONTENT

Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**PR Options:**

For QA:
```bash
gh pr create \
  --title "release(all): v2.{year}-{month}-{date}.0 정기배포 QA Release" \
  --base qa \
  --head develop \
  --assignee @me \
  --body "..."
```

For Prod:
```bash
gh pr create \
  --title "release(all): v2.{year}-{month}-{date}.0 정기배포 Prod Release" \
  --base main \
  --head qa \
  --assignee @me \
  --body "..."
```

### 9. Clean Up Temporary File

```bash
rm deployment-summary.md
```

### 10. Confirm with User

Show the PR URL and summary:
- Number of commits included
- PR link
- Deployment stage
- Target date

## Branch Strategy

```
develop → qa → main
```

- **develop**: Development branch
- **qa**: QA testing branch (deploy date = today + 2 days)
- **main**: Production branch (deploy date = today)

## Error Handling

### No commits found
```
Error: No commits found between {base} and {head}
This might mean:
- Branches are already in sync
- Need to pull latest changes from remote
```

### PR creation failed
```
Error: Failed to create PR
Possible causes:
- Insufficient permissions
- Branch protection rules
- Conflicting PR already exists
```

### Commit parsing failed
```
Warning: Could not parse commit: {commit_subject}
Skipping this commit from summary.
```

### PR number not found
```
Warning: Could not find PR number for commit: {commit_subject}
Using commit link instead: https://github.com/{owner}/{repo}/commit/{hash}
```

## Important Notes

- **Always sync branches** before getting commit history
- **Use PR links**, not commit links in the summary
- **Group commits** by domain, order, and author
- **Clean up** temporary files after PR creation
- **Verify** all commit messages follow Conventional Commits format
- **Handle missing PR numbers** gracefully with fallback to commit links
- **Format dates correctly** with leading zeros

## Git Safety Protocol

- NEVER force push
- NEVER skip hooks
- NEVER modify commit history
- DO NOT push changes (only create PR)
- READ-ONLY operations on git history
