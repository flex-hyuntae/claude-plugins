# flex-workflow

flex 프로젝트 전용 워크플로우 플러그인. QA/Prod 배포 PR 생성, 패키지 로컬 테스트 환경 설정, i18n 변환, TC 작성 및 QA 테스트를 지원합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `deploy` | QA/Prod 배포 PR을 커밋 요약(도메인별, 시간순, 작성자별)과 함께 생성 |
| `test-package` | 모노레포 패키지를 portal 프로토콜로 로컬 앱에 연결하여 테스트 |
| `add-til` | Notion TIL 데이터베이스에 오늘 배운 내용 기록 |
| `create-tickets` | 스펙 문서를 기반으로 Linear 티켓 자동 생성 및 리뷰 |
| `enrich-ticket` | QA 티켓을 인터뷰와 자동 탐색(Figma/코드)으로 구조화된 형식으로 강화 |
| `write-tc` | Linear, Figma, Notion, 코드베이스를 분석하여 QA 테스트 케이스 작성 |
| `run-qa` | 작성된 TC를 Chrome DevTools MCP로 실행하여 QA 테스트 수행 |

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

### add-til

```
/flex-workflow:add-til 모달 닫기 애니메이션을 위해 open과 type 상태를 분리해야 한다
```

또는 "오늘 배운거야", "TIL", "지식 기반에 추가해줘" 등으로 호출. Notion MCP 연결 필요.

### enrich-ticket

```
/flex-workflow:enrich-ticket CORE-1234
/flex-workflow:enrich-ticket https://linear.app/flexteam/issue/CORE-1234/bug-title
```

PM/PD가 작성한 QA 버그 티켓을 분석하고, Figma 디자인 조회 · 코드베이스 탐색 · 개발자 인터뷰를 통해 누락된 정보를 수집합니다. 최종적으로 AS-IS/TO-BE/영향 범위/코드 위치/수용 기준 구조로 티켓 설명을 업데이트합니다. Linear MCP 연결 필요.

### create-tickets

```
/flex-workflow:create-tickets
/flex-workflow:create-tickets auto-employee-number
```

`spec/{feature-name}/` 디렉토리의 스펙 문서를 읽어 Linear 티켓을 자동 생성합니다. Data modeling → UI Component → API 적용 순서로 분해하고, 자체 리뷰 후 피드백을 반영합니다. Linear MCP 연결 필요.

### write-tc

```
/flex-workflow:write-tc
/flex-workflow:write-tc https://linear.app/flex/issue/CORE-1234
```

Linear 티켓, 코드베이스 변경사항, Figma 디자인, Notion 스펙 문서를 종합 분석하여 QA 테스트 케이스를 작성합니다. TC는 Notion 또는 로컬 파일로 저장됩니다.

### run-qa

```
/flex-workflow:run-qa
/flex-workflow:run-qa https://www.notion.so/tc-document-id
```

`write-tc`로 작성된 TC 문서를 Chrome DevTools MCP로 실행합니다. 각 TC를 순서대로 실행하고, 스크린샷 기반으로 결과를 검증하여 PASS/FAIL 리포트를 생성합니다. Chrome MCP 연결 필요.
