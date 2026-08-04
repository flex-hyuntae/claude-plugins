# flex-workflow

flex 프로젝트 전용 워크플로우 플러그인. QA/Prod 배포 PR 생성, 패키지 로컬 테스트 환경 설정, dev 환경 부트스트랩, i18n 변환, 위키 기록·소화를 지원합니다.

> **Note:** 티켓 생성/강화, TC 작성, QA 테스트 관련 스킬은 [drill](../drill/) 플러그인으로 이전되었습니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `deploy` | QA/Prod 배포 PR을 커밋 요약(도메인별, 시간순, 작성자별)과 함께 생성 |
| `test-package` | 모노레포 패키지를 portal 프로토콜로 로컬 앱에 연결하여 테스트 |
| `setup-dev` | remotes-* 앱의 의존성·env·dev 서버를 한 번에 부트스트랩 |
| `add-topic` | 개인 기술 지식을 위키 `Topics/` 에 기록 |
| `add-work` | flex 내부 지식을 위키 `Work/` 에 기록 (근거 경로 + 확인 날짜 필수) |
| `digest-wiki` | 하루 마감 — Raindrop·Notion 을 `Sources/` 로 동기화하고 노트와 `↔` 로 잇기 |

### 위키 세 층

`add-topic` · `add-work` 가 담당하는 경계는 이렇다. 나머지 한 층(Spec)은 [drill](../drill/) 플러그인이 쓴다.

| 층 | 무엇 | 스킬 |
|---|---|---|
| Topic | 회사와 무관한 개인 기술 지식 | `add-topic` |
| Work Topic | flex 시스템이 실제로 어떻게 동작하나 | `add-work` |
| Spec | 프로젝트 단위 요구·결정 문서 | `/drill:plan` |

vault: `~/Projects/flex/wiki` (`flex-hyuntae/wiki`, private)

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

### add-topic

```
/flex-workflow:add-topic 모달 닫기 애니메이션을 위해 open과 type 상태를 분리해야 한다
```

또는 "오늘 배운거야", "TIL", "위키에 추가해줘" 등으로 호출. `Topics/<카테고리>/` 에 노트를 만들고 인덱스를 다시 생성한 뒤 커밋·푸시한다.

### add-work

```
/flex-workflow:add-work 데스크 에이전트가 지식관리를 참고하는 경로
```

또는 "회사 지식 정리", "Work Topic 추가" 등으로 호출. `Work/<도메인>/` 에 노트를 만든다. Topic 과 달리 **읽은 파일 경로를 `## 근거` 에 남기고 `verified` 날짜를 적는 것이 필수**다 — 코드가 정본이고 노트는 사본이라서다.

### digest-wiki

```
/flex-workflow:digest-wiki
```

또는 "하루 마감", "위키 정리", "소화하자" 등으로 호출. Raindrop·Notion 을 `Sources/` 인덱스로 동기화하고, `↔ (없음)` 인 항목을 노트와 잇는다.

