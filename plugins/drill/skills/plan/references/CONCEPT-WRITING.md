# Concept 작성 가이드 — KEEP/DROP, 좋은/나쁜 예, 자가 점검

> **단계별 질문 차원** — plan(spec/concept) = **what / why** / prepare(ticket) = **how** / write(코드) = how 따라 구현. 본 가이드는 plan 단계 산출물(spec/concept) 의 작성 기준이며, **how 어휘가 본문에 등장하면 ticket 영역으로 위임**한다.

## 포함 (KEEP) — 도메인 책임 · 단일 동작 흐름 · UX 큰 흐름 · 데이터 큰 흐름

- 도메인 정의 (이 개념이 무엇인가)
- 도메인 책임 (responsibilities)
- 도메인 규칙·정책 (business rules)
- 다른 도메인과의 관계
- 핵심 분류·상태 (도메인 어휘로)
- 사용자가 거치는 큰 단계 (추상 동사로: "연결한다" / "해제한다" / "재연결한다")

## 제외 (DROP)

- **노출 매체 / 컴포넌트 종류**: "Popover" / "Modal" / "Dialog" / "Toast" / "AlertDialog" / "Sheet" / "Tooltip" — 매체는 디자인·구현 결정으로 언제든 바뀐다. "연결 설정 Popover" → "연결 설정 뷰", "확인 Modal" → "확인 단계", "성공 Toast" → "성공 안내"
- **구현 동사 ("...가 뜬다 / 떠오른다 / 열린다")**: 노출 매체 의존 표현. 도메인 동사로 압축 ("연결한다" / "확정된다" / "안내된다")
- **노출 단위 분리·생략 결정** ("사이트 0건 → 별도 안내", "변경 없음 → 모달 skip" 같은 매체 단위 분기): 도메인 동작 자체를 바꾸는 게 아니라면 매체 결정. 도메인 분기는 "확정 시점이 다르다", "수정 동선이 다르다" 같은 동사 차원으로
- **표준 프로토콜·시스템 어휘**: `OAuth` / `토큰` / `polling` / `BE` / `세션` / `endpoint` 같은 구현 영역 어휘는 **도메인 표현으로 풀어쓴다**. 예: "OAuth 진입" → "외부 서비스 로그인", "토큰 만료" → "인증 만료", "polling" → "주기적 확인", "BE 가 ... 한다" → 시스템 주체 표현 자체를 빼고 결과만 ("자연 정리된다")
  - 단, **"비동기"** 같이 사용자에게도 자연스러운 시스템 어휘는 그대로 둬도 됨
- **UI 표현 / 위치 인용**: "리스트 상단 Callout" / "헤더 CTA 배지" / "LNB 우측 배지" / 컴포넌트 위치
- **CTA 카피 그대로 인용**: "[가져오기]" / "[확인]" / "[취소]" 같은 정확한 버튼 텍스트는 X. 다만 카피의 **의미 가져가기** (예: "다시 연결하기 동작" / "다시 연결하기 액션") 는 OK — 매체 단어("버튼")만 빠지고 행동의 의미는 살림
- **API 시그니처·필드명·코드명** (`subscribeToTask` → "재구독 호출"). **클라이언트 단일 source 필드명**(`KnowledgeConnection.status` 등) 박기 금지 — BE 단일 source 정책 자체는 도메인이라 spec 에 두되, 필드명·매핑은 구현 영역
- **서버↔클라 책임 분리 / 마이그레이션 이력**: "X 는 서버에서 내려온다 / Y 는 클라이언트가 보유" / "마이그레이션 불필요(개편 시 새 시작)" 같은 표현은 구현 영역. concept 본문 X
- **추상 메타 차원** ("X 분류 축 — A 분류 / B 분류 / 두 축은 직교한다" 같은 메타 묶음 명사): concept 은 구체적 도메인 정책으로 — "필터" / "라이프사이클" / "사이트 상태"
- **표가 자족적이면 표 외 부연 반복 금지**: 도메인 동작 칼럼이 있는 표 아래에 "X 분류는 Y 라는 뜻", "Z 의 경우 별도 안내" 같은 부연 불릿 5개 이상 누적되면 표 자체를 재설계할 신호. 표 + 도메인 경계 박스 한 줄 까지만
- **카탈로그성 표**: 동작·기능을 모두 나열한 표 (도메인 어휘 한 줄로 압축)
- **ASCII 플로우 다이어그램**: 도메인 단계 명칭은 bullet 한 줄로 충분 (시각적 plot 은 spec / 구현 영역)
- **카피·픽셀·색·아이콘**: 디자인 영역
- **선택지 열거의 우선순위·본 사이클 포함 여부**: "size selector / navigator / count 중 본 사이클" / "옵션 A / B / C 중 어떤 거" 같은 옵션 우선순위 결정은 ticket 영역. spec 은 "X 를 사용한다" 까지
- **동일 행위의 중복 노출 처리**: "본문 첨부 Callout 의 다운로드와 More 메뉴 다운로드 중복 처리" 같은 위치 다중 처리는 ticket. spec 은 "X 영역에서 다운로드 가능" 까지
- **컴포넌트 시그니처·prop 분기**: "discriminated union props" / "variant" → ticket. spec 은 도메인 분기(예: "단건 / 벌크 시나리오") 까지
- **카탈로그 항목 구체 값**: "Dropdown 항목 = ON / OFF" / "Footer paginator 4-state" — ticket 영역

## 보조 원칙

- **decision 본문 인라인 링크 금지** — 본문(개요·책임) 의 줄마다 `([Decision X](path))` 형태로 박지 않는다. 영향 받은 decision 은 **하단 §관련 Decision** 섹션의 표(날짜·요약·영향 부분) 로 모은다. 본문은 도메인 어휘로 단언, decision 추적은 한 곳에서
  - 예외: 정책 한 줄로 도메인 어휘 단언이 모호한 경우 본문 끝 `(자세한 근거: [Decision Y])` 1회 정도 허용. 한 책임 영역당 인라인 ≤ 1 권장
  - 본문에 인라인 링크가 3개 이상 누적되면 가독성 신호 — 본문은 사실만 단언으로 정리하고 링크는 §관련 Decision 으로 이관
- **서비스별 분기 위임**: 상위 concept 에 모든 서비스 분기 나열 X — 서비스 concept 으로 위임 ("서비스마다 다름. {svc} 는 [[integration-{name}]] 참고")
- **중복 작성 방지**: 같은 정책이 여러 concept 에 반복 X — 단일 source ("X 의 Y 는 [[A]] 참고")
- **줄 수 상한 없음**: 도메인 본질이 큰 경우 자연스럽게 길어질 수 있음. 다만 **verbose · 구현 디테일 · 중복**의 결과로 길어진 게 아닌지 점검

## 표·다이어그램 사용 시점

- **도메인 분류 표** (ex: 사이트 상태 5분류): 도메인 어휘 컬럼만 — UI 표기·카피 컬럼 금지
- **ASCII 플로우 다이어그램**: 프로세스성 concept 의 본질 흐름이 bullet 으로 표현되지 않을 때만. 첫 시도는 bullet
- **에지 케이스 표**: 도메인 차원 처리 (ex: "권한 회수 → 상태 격상") 만. UI 동작 카탈로그 X. 미정 항목은 "미정" 섹션으로

## 좋은 예 vs 나쁜 예

### 🚫 나쁜 예 — UI 위치 인용 + 카탈로그

```
연결 상태는 LNB 의 서비스 아이템 우측 배지, 페이지 리스트 상단 Callout,
헤더 CTA 배지에 동시 표현된다.

| 분류 | LNB 배지 | Callout 메시지 |
| connected | 연결됨 | (없음) |
| expired | 인증 만료 | "재연결이 필요해요" |
```

### ✅ 좋은 예 — 도메인 어휘

```
연결 상태는 3분류이며 **단일 source** 로 모든 노출 진입점이 동일
분류로 표현된다 ([Decision X]).

| 분류 | 의미 |
| connected | 토큰 유효 + 권한 정상 |
| expired | 토큰 만료 — 재연결 필요 |
```

### 🚫 나쁜 예 — CTA 카피 + ASCII 플로우

```
[1차 모달] → [연동하기] → OAuth → [2차 모달]
                                  ├── [확인] → 확정
                                  └── [취소] → 롤백
```

### ✅ 좋은 예 — 단계 bullet (도메인 사건)

```
- 최초 연동: OAuth → Admin 판정 → 사용자 확정 시점에 connection 생성
- 수정 시나리오: OAuth → OAuth 복귀 시점에 확정 (토큰 즉시 교체)
```

### 🚫 나쁜 예 — 노출 매체 + 구현 동사

```
연결 설정 Popover 에서 [연결 해제] 메뉴를 선택하면 AlertDialog 가
열리고, 확인 시 success Toast 가 뜬다.
```

### ✅ 좋은 예 — 추상 동작 (매체 빠짐)

```
연결 설정 뷰에서 사용자가 연결 해제를 선택하면 확인 후 해제된다.
```

### 🚫 나쁜 예 — "Popover Callout 4번째 진입점" 같은 매체 매트릭스

```
| 분류 | LNB 배지 | Callout | CTA | Popover 내부 Callout |
| expired | 에러 dot | error variant | "연결 만료" | error + 재연결 |
```

### ✅ 좋은 예 — 도메인 행동 리스트 (뷰의 책임)

```
### 연결 설정 뷰

연결 완료 후 사용자가 진입하는 연결 설정 뷰가 다루는 정보·동작:

**공통**

- 연결된 계정 정보 (계정 식별자 + 서비스별 추가 식별자)
- 현재 연결 상태 (정상 / 인증 만료 / 권한 부족)
- 연결 해제

**서비스별 추가**

- Jira 사이트별 상태 — [[integration-jira]]

연결 만료 시 재연결 진입은 별도 책임으로 [[reconnect]] 참고.
```

> **패턴 핵심**:
>
> 1. **"{X} 뷰" 또는 "{X} 단계"** 같은 매체 중립 명칭으로 부른다 (Popover / Modal X)
> 2. 헤더는 **"가지는 책임"** 이 아니라 **"다루는 정보·동작"** — 정보(명사)와 동작(동사)을 함께 담는다
> 3. **단위가 다른 항목은 그룹 분리** (`**공통**` / `**서비스별 추가**`) — 연결 1개 책임과 사이트 N개 책임을 한 bullet 리스트에 섞지 않는다
> 4. **"확인" 같은 일반 동사 회피** — 명사형(`연결된 계정 정보`)이거나 행동 동사(`연결 해제` / `재연결 진입`)로 명확히
> 5. **세부 플로우는 본문 외부로 위임** — "재연결 플로우는 [[reconnect]] 참고" 식 1줄. 같은 리스트에 항목으로도 두면서 위임도 하면 책임이 어디 있는지 모호해진다

### ✅ 좋은 예 — 단일 source 도메인 분류

```
연결 상태는 3분류이며 단일 source 로 노출된다. 어떤 진입점·매체에
표현되든 같은 분류를 따른다.
```

### 🚫 나쁜 예 — 선택지 우선순위·본 사이클 결정

```
지식 목록은 페이지네이션을 사용한다. Footer paginator 는
size selector / navigator / count 표시를 모두 노출한다 (본 사이클).

다운로드 액션은 본문 첨부 Callout 의 [다운로드] 버튼 +
사이드픽 More 메뉴 [다운로드] 항목 양쪽에서 제공한다.

AI 게시 셀의 Dropdown 항목은 ON / OFF 두 가지로 구성된다.
```

### ✅ 좋은 예 — 약속까지만, 선택은 ticket 으로 위임

```
- 지식 목록은 페이지네이션을 사용한다 — 본 사이클에 포함할 옵션(size selector / navigator / count) 은 ticket 영역
- 파일 타입은 사이드픽 안에서 다운로드 가능하다 — 노출 위치(Callout 단독 vs More 메뉴 중복) 는 ticket 영역
- AI 게시 ON / OFF 를 제어할 수 있다 — 컨트롤 표현(Dropdown / Toggle 등) 은 ticket 영역
```

### 🚫 나쁜 예 — 행위 카탈로그 + 위치 결정 혼재

```
사이드픽 More 메뉴는 5 액션을 노출한다: 복제 / 그룹 옮기기 /
다운로드 / 공유 / 삭제. 다운로드는 파일 타입에만 노출되며 본문
첨부 Callout 과 중복으로 제공된다.
```

### ✅ 좋은 예 — 동작 약속만

```
지식 문서·파일의 상세 화면에서는 다음 액션이 가능하다:
- AI 게시 ON/OFF 전환
- 그룹 옮기기
- 파일 타입의 경우 다운로드
- 삭제
- 생성자·수정자 메타 확인

각 액션의 노출 위치·진입 매체·중복 처리는 ticket 영역.
```

### 🚫 나쁜 예 — 본문 인라인 decision 링크 (가독성 저하)

```
### 콘텐츠 타입

지식은 다음 세 타입 중 하나를 가진다:

- **문서**: 텍스트 기반 에디터 지원 ([Decision 2026-05-18 import-unified-to-file-upload](../decisions/2026-05-18-import-unified-to-file-upload.md)). 외부 파일은 시스템 판단으로 자동 귀속 ([Decision 2026-05-18 file-upload-catalog-13-types](../decisions/2026-05-18-file-upload-catalog-13-types.md))
- **파일**: 원본 보존, 13종 카탈로그 ([Decision 2026-05-18 file-upload-catalog-13-types](../decisions/2026-05-18-file-upload-catalog-13-types.md)). 검증 정책은 100건·10MB·카탈로그 일치 ([Decision 2026-05-18 file-upload-validation-toast-matrix](../decisions/2026-05-18-file-upload-validation-toast-matrix.md))
- **AI 게시 OFF 시각 표식**은 제목 영역에서 다룬다 ([Decision 2026-05-18 list-columns-actions-and-ai-publish-dropdown](../decisions/2026-05-18-list-columns-actions-and-ai-publish-dropdown.md))
```

본문이 도메인 사실의 흐름이 아니라 **인라인 링크 매트릭스** 가 되어 PM/디자이너가 한 번에 읽기 어려워진다. 같은 decision 이 여러 책임 영역에서 인용되어 중복되기도 한다.

### ✅ 좋은 예 — 본문은 도메인 단언, decision 은 §관련 Decision 으로 모음

```
### 콘텐츠 타입

지식은 다음 세 타입 중 하나를 가진다:

- **문서**: 텍스트 기반 에디터 지원. 외부 파일은 시스템 판단으로 자동 귀속
- **파일**: 원본 보존, 입력 카탈로그 13 종. 검증은 개수·용량·카탈로그 일치 3 축
- AI 게시 OFF 의 시각 표식은 제목 영역에서 다룬다

(... 본문 계속 ...)

## 관련 Decision

| 날짜 | Decision | 영향 부분 |
|------|----------|-----------|
| 2026-05-18 | [import-unified-to-file-upload](../decisions/2026-05-18-import-unified-to-file-upload.md) | §콘텐츠 타입 (외부 파일 자동 귀속) |
| 2026-05-18 | [file-upload-catalog-13-types](../decisions/2026-05-18-file-upload-catalog-13-types.md) | §콘텐츠 타입 (13 종 카탈로그) |
| 2026-05-18 | [file-upload-validation-toast-matrix](../decisions/2026-05-18-file-upload-validation-toast-matrix.md) | §콘텐츠 타입 (검증 3 축) |
| 2026-05-18 | [list-columns-actions-and-ai-publish-dropdown](../decisions/2026-05-18-list-columns-actions-and-ai-publish-dropdown.md) | §AI 게시 여부 (OFF 시각 표식 위치) |
```

> **패턴 핵심**:
>
> 1. 본문은 **도메인 어휘 단언** — "지식은 N 타입을 가진다" / "입력 카탈로그 13 종"
> 2. decision 추적은 **§관련 Decision 표** 한 곳 — `날짜 / Decision / 영향 부분(§...)` 3 컬럼
> 3. SPEC.md 의 Decision Log = feature 전체 / concept 의 §관련 Decision = 본 concept 영향 서브셋 — 두 곳이 다른 책임
> 4. 본문 인라인 ≤ 1 회 권장. 3개 이상이면 이관 신호

### 🚫 나쁜 예 — 상세 화면을 컴포넌트 구조로 묘사

```
문서·파일 모두 사이드픽(fx Sheet) 으로 상세를 연다. 기본 폭 680px,
Resizer 로 확장 가능. 헤더(Title + Property + flexical toolbar) +
본문 + bottombar(저장) + More 메뉴 + AlertDialog 구성. Property
표시는 documentProperty/valueWrap 6종(label / avatar / avatarGroup /
tag(Multi) / switch / empty) 패턴. 태그 표면 컴포넌트는
tagSelectMenu / tagEditMenu(Tag / TextTag 2 유형).

> 공용 컴포넌트: 사이드픽 헤더/에디터/property/Bottombar 는
> AI Library RichPage (AID-2524) 산출물을 사용. AccessDialog 는
> AI Library AccessDialog (AID-2523) 산출물을 사용.
```

이 한 문단에 들어간 매체·구현 어휘: `사이드픽(fx Sheet)` / `680px` / `Resizer` / `Title` / `Property` / `flexical toolbar` / `bottombar` / `More` / `AlertDialog` / `documentProperty/valueWrap 6종` / `label / avatar / avatarGroup / tag(Multi) / switch / empty` / `tagSelectMenu / tagEditMenu` / `Tag / TextTag` / `RichPage (AID-2524) 산출물` / `AccessDialog (AID-2523) 산출물`. spec/concept 가 책임이 아니라 컴포넌트 사양서가 됐다.

### ✅ 좋은 예 — 상세뷰는 도메인 책임 단위로

```
### 상세뷰

문서·파일 모두 상세뷰를 제공한다. 상세뷰의 책임:

- 답변 활용 대상도 상세에서 노출·편집 — 목록과 동일한 의미·동일한 편집 진입
- 카테고리 미분류 경고가 상세의 카테고리 영역 안에서도 표현
- 단건 자주 쓰는 액션 + 작성/수정 메타는 상세에서도 동일하게 제공 — 목록·벌크·상세 세 표면 동일
- 명시적 저장 + dirty 게이트 — 자동 저장 없음, 변경된 내용 있을 때만 저장 가능, 변경된 채로 이탈 시도 시 경고
```

> **패턴 핵심**:
>
> 1. **"사이드픽" 도 매체** — 도메인은 "상세뷰". 매체 표현(side sheet / fx Sheet / Drawer 등)은 spec 에서 빠진다
> 2. **컴포넌트 구조 묘사 금지** — Title / Property / toolbar / bottombar / More 같은 part 분해는 ticket 영역
> 3. **공용 컴포넌트 매핑 금지** — "X 는 RichPage 산출물 사용" 은 ticket 의 구현 결정. spec 은 어떤 도메인 책임이 있는지만
> 4. **치수·아이콘·variant 카탈로그 금지** — 680px / 6종 / 2 유형 같은 표현은 ticket 영역

### 🚫 나쁜 예 — §미정에 잡탕 미정

```
## 미정

- 파일 뷰어 제공 여부 (현재: 사이드픽에서 메타 + 첨부 Callout + 다운로드만, 인라인 뷰어 없음)
- 사이드픽 너비 persist 정책 (사용자 마지막 너비 저장 vs 매 진입 reset)
- 동시 편집 충돌 처리 (낙관적 vs 비관적 vs 경고만)
- AI 피드백 관리 시나리오 — 별도 사이클
- More 메뉴 5 액션 카피·정렬 (Figma 라벨 합의 후)
- audience valueWrap 매핑 (avatarGroup vs tag(Multi)) — Figma 노드 합의 후
- AI 게시 비활성화 라벨 카피
- 카테고리 미분류 경고 아이콘
```

진단:
- "파일 뷰어 제공 여부" → 실제로는 **다운로드 제공이 사실**. 미정 아니라 본문에 fact 표기
- "너비 persist 정책" / "라벨 카피" / "valueWrap 매핑" / "아이콘" → 구현 판단, ticket 영역. §미정 아님
- "동시 편집 충돌 처리" → 본 사이클 outside. 본문에 "본 사이클 outside" 명시하거나 아예 §미정 X
- "AI 피드백 관리 시나리오" → 의미 불명. §미정에 두지 말고 사용자에게 의미 확인 (모르는 항목은 §미정 자격 없음)

### ✅ 좋은 예 — §미정은 본 사이클 사실 미정만

```
## 미정

- URL 속성(지식 문서/파일에 URL 보유) — 본 사이클 제외, 후속 사이클에서 재논의
```

> **§미정 자가 점검**:
>
> - **본 사이클 사실 미정** (도메인 약속이 아직 안 정해진 것) → §미정에
> - **구현 판단** (라벨·아이콘·valueWrap 매핑·너비 정책 등) → §미정 아님, ticket 영역
> - **본 사이클 outside** (동시 편집·AI 피드백 등) → 본문에 "본 사이클 outside" / "후속 사이클" 명시 또는 §미정 X
> - **사실인 약속** (다운로드 제공 등) → 미정 아니라 본문에 사실로 기재
> - **의미 불명 항목** (정의가 모호한 미정 후보) → §미정에 두지 말고 인터뷰에서 의미 확인. 모르는 항목은 §미정 자격 없음

> **패턴 핵심**:
>
> 1. **"X 를 할 수 있다"** 약속까지가 spec — "어디서 / 어떻게 / 몇 개 / 어느 순서로" 는 ticket
> 2. **선택지 우선순위 / 본 사이클 포함 여부 결정** 은 prepare 단계에서 ticket 본문이 다룬다
> 3. **동일 행위의 다중 위치 중복** 같은 결정은 ticket 영역. spec 은 "{영역} 안에서 {행위} 가능" 까지
> 4. spec 의 모호성을 결함으로 오해해서 닫으려 하지 않는다 — 의도된 자유도

## Concept 분리 vs 통합 결정 기준

도메인을 N개 concept 으로 나눌지, 단일 concept 안 sub-section 으로 둘지 결정할 때.

### 분리 권장

- **자기 책임 영역이 명확히 다름** (관계 생애 주기 vs 데이터 표현 같이) **이면서**, 각 책임의 디테일이 큰 경우
- 분리된 concept 들이 **서로의 본문을 인용하지 않고도 독립적으로 읽힘**
- 다른 도메인 (knowledge / category 등) 에서 어느 concept 을 참조할지 명확

### 통합 권장 (분리 X)

- Provider/Subtype 차이는 분리 사유가 아님 — **단일 concept 안에서 sub-section 으로** (예: `### Jira` / `### Google Calendar`)
- 관계 layer (수명 주기) 와 표현 layer (리스트 형상) 가 같은 도메인 흐름(연결 → 사용 → 표현)이면 통합 검토 — 분리 시 같은 흐름이 두 concept 에 걸쳐 흩어진다
- **"어디에 정보가 있어야 할지 헷갈리면 통합"** — 독자가 같은 사실을 두 곳에서 찾아야 하면 분리 비용이 가치보다 큼
- 한 concept 의 본문이 다른 concept 본문을 **여러 번** 참조해야 자명해지면 통합 신호

### 실제 정리 사례

- **integration / integration-jira / integration-knowledge** (3 concept) → **integration** (1 concept, 4부 구조) 통합 — 같은 도메인 흐름(연결 → 사용 → 표현)이고 Provider 차이는 sub-section 으로 충분. 분리 시 사용자가 "Jira 만 검색·필터 제공" 같은 정보가 어느 concept 에 있는지 헷갈림

## 자가 점검 키워드

다음 단어들이 본문에 등장하면 매체 또는 구현 어휘다. 도메인 표현으로 다시 쓴다.

### 매체·컴포넌트 (UI 위젯)

- **fx2 디자인 시스템 컴포넌트** — `Popover` / `Modal` / `Dialog` / `Toast` / `Sheet` / `Tooltip` / `AlertDialog` / `Dropdown` / `Callout` / `Searchfield` / `BulkActionbar` / `Sidebar` / `Bottombar` / `Titlebar` / `Snackbar` / `Banner` / `Drawer` / `Panel`
- **fx 접두사 패턴** — `fx*` / `Fx2*` / `flexical` 로 시작하는 모든 이름 (예: `fx Sheet`, `fx Tag`, `Fx2Button`, `flexical toolbar`)
- **사이드픽·사이드시트** — `사이드픽` / `사이드시트` / `side sheet` 같은 패턴명 자체가 매체 (도메인은 "상세뷰")
- **매체 동사**: `"뜬다"` / `"열린다"` / `"닫힌다"` / `"슬라이드인"` / `"열리면서"` / `"펼쳐진다"`

### 컴포넌트 내부 part · slot · variant

- **part / slot 이름** — `valueWrap` / `documentProperty` / `documentHeader` / `tagSelectMenu` / `tagEditMenu` / `startSlot` / `endSlot` / `actionSlot` / `primaryWrapper` / `itemSlot` / `contentSlot` / `parts/*` / `footer` (컴포넌트 안 영역명)
- **variant·variant 카탈로그** — `valueWrap 6종` / `4-state` / `3 variant` / `True/False variant` / `info/warning/error variant`
- **변형 키워드** — `solid=false` / `type=default` / `size=small` 같은 prop 표기

### 치수·픽셀·디자인 토큰

- **픽셀·치수** — `680px` / `1080px` / `최소 너비` / `최대 너비` / `폭 N`
- **디자인 토큰** — `text/primary` / `var(--xxx)` / `text/quaternary` / `base.red.red500` / `border/tertiary`
- **색 이름·아이콘 이름** — `red500` / `green` / `DashedcircleIcon` / `ArrowCornerDownRightIcon`

### 사내 시스템·구현 어휘

- **구현 영역** — `OAuth` / `토큰` / `polling` / `BE` / `endpoint` / `필드명` / `엔티티`
- **사내 시스템 모듈·인프라** — `매트릭스` / `매트릭스 적재` / `connector` / `connector 모듈` / `매핑 테이블` / `적재 파이프라인`
- **책임 분리 이력** — `"서버에서 내려온다"` / `"클라이언트가 보유"` / `"마이그레이션"` / `"BE 와 1:1 매핑"`
- **추상 메타** — `"분류 축"` / `"직교"` / `"단일 source 필드"` / `"두 도메인 축"`

### Ticket·산출물 매핑

- **ticket id** — `AID-\d+` / `AGE-\d+` / 그 외 jira/linear ticket prefix
- **공용 컴포넌트·산출물 이름** — `RichPage` / `AccessDialog` / `AI Library` / `RichPage 산출물` / `AccessDialog 산출물` / `"X 의 Y 산출물 사용"` 같은 ticket 매핑 표기 자체

### UI 상태·정책

- **상태 관리 정책** — `persist` / `세션 단위 vs 영구` / `초기값` / `default 상태` / `최초 진입 시` / `너비 정책` / `높이 정책` / `리사이즈 정책`
- **인터랙션 단계** — `hover` / `focus` / `active` / `disabled state` / `dim 처리` / `preselected` / `preselection`

### 매체 분기·선택지·카탈로그·중복

- **매체 분기 결정** — `"X 0건 → 별도 안내"` / `"변경 없음 → Y skip"` (매체 결정, 도메인 동작이 아니면 X)
- **선택지·옵션 카탈로그** — `"옵션 A / B / C"` / `"본 사이클 포함"` / `"3 항목 중"` / `"size selector / navigator"` (우선순위 결정은 ticket 영역)
- **위치 중복 결정** — `"X 와 Y 양쪽에서 제공"` / `"Callout 과 More 메뉴 중복"` / `"진입점 N 개"` (위치 결정은 ticket 영역)
- **카탈로그 항목 구체 값** — `"Dropdown 항목 = ON / OFF"` / `"4-state"` / `"5 액션"` (카탈로그는 ticket 영역)
- **시그니처·prop 분기 어휘** — `"discriminated union"` / `"variant prop"` / `"prop 시그니처"` (구현 영역)
- **본문 인라인 decision 링크 누적** — 한 책임 영역에 `[Decision X](path)` 인라인이 2 회 이상 보이면 §관련 Decision 으로 이관. 본문은 도메인 단언으로 정리
- **how 어휘 새어들어옴** — `"어떻게"` / `"어디에"` / `"어떤 매체"` / `"어떤 항목"` / `"어떤 prop"` 같은 how 차원 단어가 본문에 등장하면 ticket 영역. 본 단계는 **what (무엇을 할 수 있다) + why (왜 그래야 하는가)** 만

### 표현 정확성 함정

다음 표현은 사실 확인 후 정정한다:

- **`"X 진입점이 제거되었다"`** — 사용자가 X 동작을 못 하게 되었는지(=진짜 제거) vs Y 흐름으로 흡수됐는지(=통합) 확인. 후자라면 `"X 는 Y 흐름으로 통합"` / `"X 진입점을 별도로 두지 않고 시스템 판단으로 Y 에 자동 귀속"` 같이 정확한 표현
- **`"X 가 폐기"`** / **`"X 미지원"`** — 진짜 사용자가 X 를 할 수 없게 됐는지 vs 다른 방식으로 같은 결과를 얻는지 확인
- **`"매트릭스 적재 및 X"`** — 사내 시스템 어휘. 사용자 약속(`"에이전트가 답변에 활용 가능"` / `"AI 답변에 사용 가능"`)으로 치환

### 치환 예

| 잘못된 표현 | 도메인 표현 |
|------------|-------------|
| `OAuth` | `외부 서비스 로그인` |
| `토큰 만료` | `인증 만료` |
| `polling` | `주기적 확인` |
| `분류 축` | `필터` 또는 `라이프사이클` |
| `사이드픽(fx Sheet) 으로 상세를 연다` | `상세뷰를 제공한다` |
| `fx Searchfield 토글 진입` | `검색이 가능하다` |
| `BulkActionbar` | `벌크` 또는 본문에서 빼고 §[[knowledge]] 행동 참조 |
| `매트릭스 적재 및 에이전트 사용 허용` | `에이전트가 답변에 활용 가능하게 허용` |
| `valueWrap 6종 (label / avatar / ...)` | (spec 에서 제거 — ticket 영역) |
| `documentProperty / tagSelectMenu / tagEditMenu` | (spec 에서 제거 — ticket 영역) |
| `RichPage (AID-2524) 산출물 사용` | (spec 에서 제거 — ticket 영역, 어떤 공용 컴포넌트를 쓸지는 prepare 단계 결정) |
| `680px, Resizer 로 확장 가능` | (spec 에서 제거 — ticket 영역) |
| `Footer paginator 는 size selector / navigator / count 노출` | `지식 목록은 페이지네이션을 사용한다 (옵션은 ticket)` |
| `Callout 과 More 메뉴 중복 다운로드` | `사이드픽 안에서 다운로드 가능 (위치는 ticket)` |
| `Dropdown 항목 = ON/OFF` | `AI 게시 ON/OFF 제어 가능 (컨트롤 표현은 ticket)` |
| `가져오기 진입점은 제거` | `외부 파일을 가져오는 별도 진입점은 두지 않는다 — 시스템 판단으로 문서/파일 자동 귀속` |

### 변경 cascade 판정

다음 변경은 **spec cascade 가 아니라 ticket 영역**의 변경이다 — spec 본문은 손대지 않는다:

- **매체 변경** (Modal → Popover, Sheet → Drawer)
- **선택지 변경** (size selector 포함 여부, 옵션 3개 → 5개)
- **위치 변경** (More 메뉴에 항목 추가, Callout 옆으로 이동)
- **컴포넌트 매핑 변경** (AI Library RichPage 사용 → 자체 구현)
- **치수·padding·아이콘 변경**
- **카피 변경** (제외: 도메인 어휘를 바꾸는 카피는 spec 영역)
