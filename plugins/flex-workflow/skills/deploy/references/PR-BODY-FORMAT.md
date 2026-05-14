# Deployment PR Body Format

## Commit Parsing

각 커밋의 subject를 `<type>(<domain>): <message> (#<pr-number>)` 형태로 파싱한다.

예: `fix(objective): fix issue with objective (#4156)`
- type: `fix`
- domain: `objective`
- message: `fix issue with objective`
- pr_number: `4156`

PR 번호 추출:
1. `(#XXXX)` 패턴을 subject에서 추출
2. 없으면 commit message로 GitHub 검색
3. 끝까지 못 찾으면 commit link로 fallback (`Warning: Could not find PR number for commit: ...`)

커밋 데이터 구조:

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

## PR Body 구조 — 3개 섹션

### Section 1: Domains (도메인별 그룹핑)

```markdown
# Domains
## objective
- [fix: fix issue with objective](https://github.com/{owner}/{repo}/pull/4156)
- [feat: add new objective feature](https://github.com/{owner}/{repo}/pull/4157)
## user
- [fix: fix user authentication bug](https://github.com/{owner}/{repo}/pull/4158)
```

### Section 2: Orders (시간순 전체 리스트)

```markdown
# Orders
- [fix: fix issue with objective](https://github.com/{owner}/{repo}/pull/4156)
- [feat: add new objective feature](https://github.com/{owner}/{repo}/pull/4157)
- [fix: fix user authentication bug](https://github.com/{owner}/{repo}/pull/4158)
```

### Section 3: Authors (작성자별 그룹핑)

```markdown
# Authors
## John Doe
- [fix: fix issue with objective](https://github.com/{owner}/{repo}/pull/4156)
- [feat: add new objective feature](https://github.com/{owner}/{repo}/pull/4157)
## Jane Smith
- [fix: fix user authentication bug](https://github.com/{owner}/{repo}/pull/4158)
```

## Summary 파일 생성 및 PR 본문 주입

```bash
# 임시 파일 생성
cat > deployment-summary.md <<'EOF'
# Domains
...

# Orders
...

# Authors
...
EOF
```

PR 생성 시 본문 주입 (변수 경유로 따옴표 안전):

```bash
BODY_CONTENT=$(cat deployment-summary.md)
gh pr create --title "..." --base qa --head develop --assignee @me --body "$BODY_CONTENT

Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## PR 옵션

**QA**:

```bash
gh pr create \
  --title "release(all): v2.{year}-{month}-{date}.0 정기배포 QA Release" \
  --base qa \
  --head develop \
  --assignee @me \
  --body "..."
```

**Prod**:

```bash
gh pr create \
  --title "release(all): v2.{year}-{month}-{date}.0 정기배포 Prod Release" \
  --base main \
  --head qa \
  --assignee @me \
  --body "..."
```

## 처리 가이드

- PR 생성 직후 `rm deployment-summary.md` 로 임시 파일 정리
- commit message가 Conventional Commits 형식이 아니면 `Warning: Could not parse commit: {subject}` 출력 후 해당 커밋만 skip
- PR 번호 못 찾으면 commit link로 fallback
- 날짜는 leading zero 포함 (`v2.2026-01-15.0`)
