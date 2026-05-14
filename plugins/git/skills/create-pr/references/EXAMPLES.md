# Pull Request Examples

## PR Title — Good

- `feat(goal): 목표 데이터 엑셀 내보내기 기능 추가`
- `fix(auth): 토큰 만료 처리 오류 수정`
- `refactor(user-profile): search-with-approval API 사용`
- `chore(deps): react-query v5 업데이트`

## PR Title — Bad

scope 누락, 길이 초과, 구현 디테일 노출이 흔한 실수:

- `refactor: 경력/학력/가족 조회 API를 search-with-approval로 변경` — scope 없음, 너무 김, 구현 디테일
- `Fix bug` — scope 없음, 구체적이지 않음
- `feat: 사용자를 위한 새로운 기능 추가` — scope 없음
- `refactor(remotes-user-profile): 기존 search API를 search-with-approval로 변경하여 승인 처리 개선` — 길이 초과, 너무 상세

## Full PR Example — Feature Addition

**Title:**

```
feat(goal): 목표 데이터 엑셀 내보내기 기능 추가
```

**Description:**

```markdown
# 📝 변경 사항

## 개요

목표 데이터를 Excel 파일로 내보낼 수 있는 기능을 추가했습니다.

## as-is

- 목표 데이터를 외부로 추출하려면 수동으로 복사/붙여넣기 해야 했습니다.
- 대량의 데이터를 다루기 어려웠습니다.

## to-be

- Excel 내보내기 버튼을 클릭하면 현재 필터된 목표 데이터를 Excel 파일로 다운로드할 수 있습니다.
- 모든 컬럼과 포맷이 유지됩니다.
- 에러 처리 및 성공 알림이 포함되어 있습니다.

# 🔗 같이 보면 좋아요

## design

https://www.figma.com/file/xxxxx

## slack

https://flexhq.slack.com/archives/xxxxx
```

## Subject 작성 가이드

- 한글 명사형/동사형 종결 ("추가", "수정", "변경")
- 72자 이하
- 마침표 없음
- 구현 디테일은 description으로, subject는 WHAT
- 간결하게: "X API 사용" not "기존 Y API를 X API로 변경하여 승인 처리 개선"
