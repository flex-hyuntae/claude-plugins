# Commit Message Examples

## Good Examples

### Feature Addition

```
feat(goal): 목표 데이터 엑셀 내보내기 기능 추가

목표 데이터를 Excel 파일로 내보내는 버튼과 API 연동을 추가.
에러 처리 및 성공 알림 포함.

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Bug Fix

```
fix(auth): 토큰 만료 처리 오류 수정

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Chore

```
chore(deps): react-query v5.0.0 업데이트

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Refactoring

```
refactor(review): 리뷰 코멘트 로직을 커스텀 훅으로 분리

복잡한 코멘트 처리 로직을 useReviewComments 훅으로 분리하여
테스트 용이성과 재사용성 개선.

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Bad Examples — Missing Scope

scope가 빠지면 PR 검색·changelog 자동화·코드 오너 매핑이 모두 깨진다. 항상 포함한다.

```
# WRONG
refactor: 리뷰 코멘트 로직을 커스텀 훅으로 분리
fix: 토큰 만료 처리 오류 수정

# CORRECT
refactor(review): 리뷰 코멘트 로직을 커스텀 훅으로 분리
fix(auth): 토큰 만료 처리 오류 수정
```

## Scope 추출 패턴

| 변경 경로 | scope |
|----------|-------|
| `apps/remotes-goal/...` | `goal` |
| `apps/remotes-evaluation/...` | `evaluation` |
| `packages/core-*-hooks/...` | `core-hooks` |
| `packages/auth/...` | `auth` |
| 여러 도메인 동시 변경 | `all` |
| `package.json`, `yarn.lock` 등 의존성 | `deps` |
