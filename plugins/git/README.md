# git

Git 워크플로우 자동화 플러그인. Conventional commit 형식의 커밋 메시지 생성, GitHub PR 자동 생성, stacked PR rebase 정리를 지원합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `git-commit` | git diff/log를 분석하여 conventional commit 형식의 커밋 메시지 생성 |
| `github-pr` | 브랜치 변경사항을 분석하여 GitHub PR 자동 생성 (한국어 설명) |
| `git-rebase-stack` | stacked PR에서 base branch merge 후 나머지 branch들을 순차 rebase |

## 사용 예시

### git-commit

```
/commit
```

스테이징된 파일 또는 수정된 파일을 분석하여 conventional commit 메시지를 생성합니다.

### github-pr

```
/pr
/pr --draft
```

현재 브랜치의 모든 커밋을 분석하여 PR 제목(conventional commit)과 한국어 설명을 자동 생성합니다. PR 생성 전 type-check/lint/test 검증을 수행하고, 대화에서 학습 포인트를 정리합니다.

### git-rebase-stack

```
/rebase-stack develop feat/B feat/C
```

develop 위로 feat/B를 rebase하고, rebased feat/B 위로 feat/C를 rebase합니다.
