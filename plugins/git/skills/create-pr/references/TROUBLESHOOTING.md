# PR Creation Troubleshooting

## 사전 안전 체크

PR 생성 전에 다음을 확인하고, 위반 시 사용자에게 알리고 중단한다:

- 현재 브랜치가 `develop`, `qa`, `main` 이 아닐 것 (보호 브랜치에 직접 PR 금지)
- base branch 대비 commit이 1개 이상 있을 것
- uncommitted 변경 사항이 없을 것 (있으면 경고)
- 브랜치가 remote에 push 되어 있을 것 (없으면 push 제안)
- GitHub 인증이 활성 상태일 것

브랜치가 remote에 없으면:

```bash
git push -u origin <current-branch>
```

## PR 생성 실패 시 대응

| 증상 | 원인·대응 |
|------|----------|
| `gh: not authenticated` | `gh auth login` 안내 |
| `head branch not found on remote` | 위 `git push -u origin` 안내 |
| `pull request already exists` | 기존 PR URL 안내, 업데이트 여부 확인 |
| `permission denied` | 레포 권한 확인 안내 |
| type-check / lint / test 실패 | 오류 메시지 그대로 보여주고 PR 생성 중단, 수정 후 재시도 안내 |

## 완료 검증 게이트 상세

PR 생성 직전 변경된 패키지를 자동 감지하고 검증:

```bash
# 변경 파일 → 패키지 추출
git diff origin/develop..HEAD --name-only | grep -oP 'apps/[^/]+' | sort -u

# 감지된 각 패키지 검증
yarn turbo run type-check --filter=@flex-apps/{package-name}
yarn turbo run lint --filter=@flex-apps/{package-name}
yarn turbo run test --filter=@flex-apps/{package-name}
```

- 모두 통과 → 진행
- 실패 항목 있음 → 오류 표시 + PR 생성 중단
- `test` 스크립트 미존재 → 경고만 표시하고 진행

## Learnings Summary 처리

PR 생성 직전 현재 대화를 리뷰하여 학습 포인트를 **메시지로** 사용자에게 전달한다 (PR 본문에 넣지 않음).

**수집 대상:**

1. **Claude가 다르게 접근한 부분**: 사용자가 Claude의 코드나 접근 방식을 수정/거부한 경우
2. **사용자가 명시한 학습 포인트**: "이건 기억해", "앞으로는 이렇게 해" 등 명시적 언급

**출력 형식:**

```
## 학습 포인트 정리

### Claude가 다르게 접근한 부분
- [상황]: [Claude의 접근] → [사용자의 수정]

### 사용자가 명시한 포인트
- [내용]

> CLAUDE.md에 반영할 내용이 있다면 알려주세요.
```

학습 포인트가 없으면 이 섹션 자체를 건너뛴다. PR 본문에는 절대 포함하지 않는다.
