# Stack — FE / BE 차이만

drill 의 절차·게이트·문서 형식은 stack 과 무관하다. stack 이 갈리는 지점은 아래뿐이다.

## 감지

레포 루트 기준. 판별 불가면 AskUserQuestion.

| 신호 | stack |
|------|-------|
| `settings.gradle.kts` / `build.gradle.kts` | BE |
| `package.json` + `turbo.json` | FE |

한 feature 가 두 레포에 걸치면 spec 은 하나(`til/spec/{feature}/`), 티켓은 stack 별로 발급하고 FE `[API]` 를 BE 티켓 `blockedBy` 로 잇는다. worktree·PR 은 레포별.

## 티켓 분해 축

`[플로우]` / `[마크업]` / `[API]` 3축은 stack 공용 — 정의는 `prepare` §FE 3방향 분해.

**BE 는 3축에 억지로 맞추지 않는다.**

- `[플로우]` 는 BE 에서도 쓴다 — use-case·정책·상태 전이가 곧 플로우
- `[마크업]` 은 BE 에 해당 없음 (repository·DDL 을 여기 매핑하지 않는다)
- 그 외 BE 작업은 **prefix 없이** 작은 완결 단위로 발급. 축 추가는 감이 잡힌 뒤에

## 검증 (`write` §4)

- **FE**: `yarn turbo run type-check --filter=@flex-apps/{pkg}` · `lint` 동일 필터
- **BE**: `./gradlew :{domain}:{module}:compileKotlin` · `ktlintCheck` · `test`

## 의존 방향 (`write` §바깥 → 안 단방향)

원칙은 동일 — 휘발성 바깥이 안정 코어에 안정 인터페이스로만 의존, 역방향 금지.

- **FE**: 표현(마크업·스타일) → 데이터 흐름(뷰 모델·훅·query). 서버 응답 형태가 표현으로 새지 않게 경계에서 뷰 모델로 변환
- **BE**: 헥사고날 의존 방향 그대로 — 어댑터(`repository-{type}`·`message-queue-{type}`)·driving(`api`) → 포트(`infrastructure`) → 순수 도메인(`model`·`service`). 규칙 본문은 `module-structure.md` (아래 위임)

## BE 컨벤션 위임

drill 은 BE 컨벤션을 갖지 않는다. `backend-guidelines-doc-loader` agent 에 `use_when` 태그를 넘겨 필요한 문서만 로드한다 (플러그인 미설치면 생략하고 진행).

| 단계 | 넘길 태그 |
|------|----------|
| `prepare` 구현 설계 | `module-structure` · `api-design` · `error-handling` · `data-modeling` · DDL 있으면 `liquibase` |
| `write` 작성 | 위 + `spring-conventions` · `testing-policy` |
| `ship` 커밋·PR | `pr-conventions` · `branching-and-versioning` |
| `qa` TC | `api-design` · `error-handling` · `testing-policy` |

## QA selector (`drill-qa` §5)

- **FE**: DOM 기준 — 버튼 텍스트·`aria-*`·`input[name]`. Chrome DevTools MCP 실행 가능 수준
- **BE**: HTTP 계약 기준 — `{method} {path}` · 요청 body · 기대 status · 응답 필드 · 실패 시 `FlexError` 코드. 실행 수단은 통합 테스트 또는 HTTP 클라이언트
