# flex-workflow

Flex 프로젝트 전용 워크플로우 플러그인. QA/Prod 배포 PR 생성, 패키지 로컬 테스트 환경 설정, i18n 변환을 지원합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `deploy` | QA/Prod 배포 PR을 커밋 요약(도메인별, 시간순, 작성자별)과 함께 생성 |
| `test-package` | 모노레포 패키지를 portal 프로토콜로 로컬 앱에 연결하여 테스트 |

## 에이전트

| 에이전트 | 설명 |
|----------|------|
| `i18n-convert` | 하드코딩된 텍스트를 i18n 번역 키로 변환 (ko/en 동시 업데이트) |

> 에이전트는 슬래시 커맨드가 아닌, 사용자의 의도를 인식하여 자동으로 실행됩니다.

## 사용 예시

### deploy

```
/flex-workflow:deploy qa
/flex-workflow:deploy prod
```

- QA: develop → qa, 배포일 = 오늘 + 2일
- Prod: qa → main, 배포일 = 오늘

### test-package

```
/flex-workflow:test-package
```

대화형으로 패키지 레포, 패키지명, 앱 경로를 입력받아 portal 연결을 설정합니다.

### i18n-convert

```
i18n 변환 해줘
하드코딩된 텍스트를 i18n으로 변환해줘
```

하드코딩된 텍스트를 식별하고, 번역 키를 생성하여 ko/en 번역 파일과 컴포넌트 코드를 업데이트합니다.
