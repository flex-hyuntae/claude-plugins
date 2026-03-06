# plan

프로젝트 기획 지원 플러그인. 심층 인터뷰를 통해 기술 스펙 문서를 자동 생성하고, Linear 티켓을 생성/리뷰합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `deep-interview` | 기술 구현, UI/UX, 우려사항, 트레이드오프에 대한 심층 인터뷰 진행 후 스펙 문서 작성 |
| `create-tickets` | 스펙 문서를 기반으로 Linear 티켓 자동 생성 및 리뷰 |

## 사용 예시

### deep-interview

```
/plan:deep-interview
/plan:deep-interview 목표 관리 엑셀 다운로드 기능
```

한국어로 심층 질문을 진행하고, 완료 후 `spec/{feature-name}/` 디렉토리에 스펙 문서를 생성합니다.

### create-tickets

```
/plan:create-tickets
/plan:create-tickets auto-employee-number
```

`spec/{feature-name}/` 디렉토리의 스펙 문서를 읽어 Linear 티켓을 자동 생성합니다. Data modeling → UI Component → API 적용 순서로 분해하고, 자체 리뷰 후 피드백을 반영합니다.
