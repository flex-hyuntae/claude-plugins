---
name: deploy
description: 'QA/Prod 배포 PR을 커밋 요약과 함께 자동 생성한다. 사용자가 "deploy qa", "deploy prod", "/deploy", "배포 PR 만들어줘", "QA 배포", "프로덕션 배포"를 요청할 때 트리거. develop→qa, qa→main 브랜치 전략 가정. PR 제목은 v2.YYYY-MM-DD.0 형식, 본문은 도메인·오더·작성자별로 정리된 커밋 요약.'
compatibility: 'gh CLI + develop/qa/main 브랜치 전략을 따르는 레포'
disable-model-invocation: true
argument-hint: "[qa|prod]"
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

### 5. Parse Commits, Build PR Body, Create PR

각 commit을 `<type>(<domain>): <message> (#<pr-number>)` 로 파싱해 도메인·오더·작성자별로 정리한 PR 본문을 만든다. 임시 파일(`deployment-summary.md`)에 본문을 작성하고 `gh pr create` 로 PR 생성, 생성 직후 임시 파일을 삭제한다.

상세한 파싱 규칙·PR 본문 3섹션 포맷·gh pr create 옵션·에러 fallback은 [references/PR-BODY-FORMAT.md](references/PR-BODY-FORMAT.md) 참고.

### 6. Confirm with User

PR URL과 요약을 표시: 포함 commit 수, PR 링크, 배포 stage(qa/prod), 타겟 날짜.

## Branch Strategy

```
develop → qa → main
```

- **develop**: 개발 브랜치
- **qa**: QA 테스팅 브랜치 (deploy date = today + 2 days)
- **main**: 프로덕션 브랜치 (deploy date = today)

## Important Notes

- 항상 base/head 브랜치 모두 remote와 sync한 후 진행
- 요약에는 PR 링크 사용 (commit 링크는 PR 번호 없을 때만 fallback)
- 날짜는 leading zero 포함 (`v2.2026-01-15.0`)
- 임시 파일은 PR 생성 후 정리

## Git Safety Protocol

force push·hook skip·history 변조는 사용하지 않는다. 이 skill은 git history에 대해 read-only로 동작하고, PR 생성만 수행한다 (브랜치 push는 하지 않음).

## Error Handling

- **No commits found** between base/head → 브랜치가 이미 sync된 상태이거나 remote pull 필요. 사용자에게 안내.
- **PR creation failed** → 권한·브랜치 보호·기존 PR 충돌 등 가능성을 사용자에게 안내.
- **Commit parsing/PR number 실패** → 해당 commit만 warning + skip 또는 commit link fallback. 자세한 fallback 메시지는 [references/PR-BODY-FORMAT.md](references/PR-BODY-FORMAT.md).
