# plan

프로젝트 기획 지원 플러그인. 심층 인터뷰를 통해 기술 스펙 문서를 자동 생성합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `deep-interview` | 기술 구현, UI/UX, 우려사항, 트레이드오프에 대한 심층 인터뷰 진행 후 스펙 문서 작성 |

## 사용 예시

### deep-interview

```
/plan:deep-interview
/plan:deep-interview 목표 관리 엑셀 다운로드 기능
```

한국어로 심층 질문을 진행하고, 완료 후 `spec-[project-name]-[YYYYMMDD].md` 형식의 스펙 문서를 생성합니다.
