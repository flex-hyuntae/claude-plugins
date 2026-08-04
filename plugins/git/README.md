# git

Git 워크플로우 자동화 플러그인. Conventional commit 형식의 커밋 메시지 생성, GitHub PR 자동 생성, stacked PR rebase 정리를 지원합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `commit` | git diff/log를 분석하여 conventional commit 형식의 커밋 메시지 생성 |
| `create-pr` | 브랜치 변경사항을 분석하여 GitHub PR 자동 생성 (한국어 설명) |
| `rebase-stack` | stacked PR에서 base branch merge 후 나머지 branch 정리 — `gh stack` 위임, 없으면 수동 순차 rebase |

## 사용 예시

### commit

```
/git:commit
```

스테이징된 파일 또는 수정된 파일을 분석하여 conventional commit 메시지를 생성합니다.

### create-pr

```
/git:create-pr
/git:create-pr --draft
```

현재 브랜치의 모든 커밋을 분석하여 PR 제목(conventional commit)과 한국어 설명을 자동 생성합니다. PR 생성 전 type-check/lint/test 검증을 수행하고, 대화에서 학습 포인트를 정리합니다.

### rebase-stack

```
/git:rebase-stack develop feat/B feat/C
```

GitHub 네이티브 stack(`gh stack` extension)이 있으면 `gh stack sync` 로 cascading rebase 를 위임합니다 — 앞 PR 이 머지됐으면 자동으로 `--onto` 모드로 전환하므로 squash merge 판정이 필요 없습니다.

extension 이 없으면 수동 폴백: develop 위로 feat/B 를 rebase 하고, rebased feat/B 위로 feat/C 를 rebase 합니다.

```
gh extension install github/gh-stack   # 권장 (public preview)
```
