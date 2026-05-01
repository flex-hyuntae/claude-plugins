---
name: plan
description: 심층 인터뷰를 통해 Spec(Index) + Concepts(개별 개념 명세)를 작성합니다
disable-model-invocation: true
argument-hint: "[주제 텍스트|linear-url|notion-url|figma-url]"
---

# Plan

심층 인터뷰로 문제를 파악하고 기능을 Concept 단위로 분해. Spec + Concept 문서 작성.

## 출력

```
~/Projects/flex/til/spec/{feature-name}/
├── {FEATURE-NAME}.md    # Index (대문자)
└── concepts/
    └── {name}.md
```

## Workflow

### 1. 주제 수집

- 사용자 입력: 텍스트 / Linear URL / Notion URL / Figma URL
- **URL 하나라도 있으면** `drill-plan-source` agent에 위임 (원본이 메인 컨텍스트 오염 방지)
- 텍스트만 있으면 skill에서 직접 처리
- `~/Projects/flex/til/spec/` 에서 관련 기존 스펙 Glob으로 확인

**Agent 호출 (URL 있을 때)**: `Task` 로 `drill-plan-source` 호출. prompt에 `linear_url / notion_url / figma_url / raw_text` 전달. agent의 `# Drill Plan Source Report` 를 **Phase 2 이후 인터뷰 배경 자료**로 사용. 원본 URL은 기록만, re-fetch는 꼭 필요할 때만.

주제 불명확하면 AskUserQuestion.

### 2. 문제 정의 인터뷰

**목표**: 왜 / 누구를 위해 / 어떤 문제를 해결하는가.

질문 방향: 현재 겪는 문제 · 불편 · 이 기능으로 창출할 가치 · 성공 기준.

한국어 AskUserQuestion, 답변에 따라 follow-up, 정의 명확해질 때까지 반복.

### 3. 도메인 심층 인터뷰

**목표**: 각 Concept이 `templates/CONCEPT.md` 섹션(개요·책임·에지 케이스·관련 Concept)을 채울 수준으로 구체화.

**카테고리**: 도메인 모델 · 구조·분류 · 프로세스 · 정책·권한 · 에지 케이스.

**각 카테고리에서 잡아야 할 축:**

| 축 | CONCEPT 섹션 | 예시 |
|----|-------------|------|
| 정체성 | 개요 | "한 문장 정의?", "왜 별도 개념?" |
| 책임·경계 | 책임 | "담당 / 담당 않는 것?" |
| 규칙/플로우 | 책임 | 모델·구조·정책 규칙 / 프로세스 플로우 |
| 관계·차이 | 관련 Concept | "다른 개념과 구분·의존·영향?" |
| 경계 상황 | 에지 케이스 | "예외·빈·삭제·만료?" |

**가이드라인**:
- **구현 상세 금지** — 자세한 추상 수준은 §6 작성 원칙
- 두 개념이 붙었다 떨어졌다 하면 결정적 차이 집중 질문 ("폴더와 카테고리 차이?")
- "왜?"를 3번 이상 물어볼 깊이
- 피상적·기술 스택 질문 금지
- UI 표현·화면 인터랙션 질문 금지 (티켓·디자인 영역)

### 4. Concept 식별

**유형**: 모델 / 구조 / 프로세스 / 정책.

**기준**: 온전한 도메인 개념 단위 (개발 단위 아님) · 독립 설명 가능 · Concept 간 관계 명확.

**절차**: 답변에서 도메인 개념 추출 → 유사 클러스터링 → 이름 부여 → 관계 파악.

### 5. Concept 확인

식별 목록을 사용자에게 제시하고 AskUserQuestion으로 합치기/분리/이름변경/추가 반영.

### 6. 문서 작성

**{FEATURE-NAME}.md** (`templates/SPEC.md` 기반, 파일명·제목 모두 대문자):
- 문제 정의 (Phase 2 수집)
- 전체 동작
- Concepts 테이블 (각 concept 링크)
- **Concept 연결**: 하이픈 리스트로 `[name](concepts/name.md) → [name](concepts/name.md): 설명` — 코드블럭 내 `[[concept]]` 단독은 렌더 안 되므로 금지
- Decision Log (빈 테이블) — plan에서는 엔트리 채우지 않음. review 단계에서 작성
- 피그마/노션 참조 링크

**concepts/{name}.md** (`templates/CONCEPT.md` 기반):
- 개요 (한두 문장 정의 + 왜 별도 concept 인지) / 책임 (도메인 어휘) / 관련 Concept / 미정

**원칙**:

concept 의 본질은 **도메인 책임·규칙·관계**.

spec / concept / decision 어느 곳에도 **구현 디테일·UI 표현·동작 카탈로그는 두지 않는다** — 티켓·디자인 산출물의 몫.

- **단일 책임** / 필요 시 책임 확장 / 다른 concept 영향은 `[[concept]]` 표시
- **포함 (KEEP)**:
  - 도메인 정의 (이 개념이 무엇인가)
  - 도메인 책임 (responsibilities)
  - 도메인 규칙·정책 (business rules)
  - 다른 도메인과의 관계
  - 핵심 분류·상태 (도메인 어휘로)
- **제외 (DROP)**:
  - **UI 표현 / 위치 인용**: "리스트 상단 Callout" / "헤더 CTA 배지" / "LNB 우측 배지" / 컴포넌트 위치
  - **CTA 카피**: 버튼 텍스트 인용 ("[가져오기]" / "[확인]" / "[취소]")
  - **API 시그니처·필드명·코드명** (`subscribeToTask` → "재구독 호출")
  - **카탈로그성 표**: 동작·기능을 모두 나열한 표 (도메인 어휘 한 줄로 압축)
  - **ASCII 플로우 다이어그램**: 도메인 단계 명칭은 bullet 한 줄로 충분 (시각적 plot 은 spec / 구현 영역)
  - **카피·픽셀·색·아이콘**: 디자인 영역
- **decision 본문 인용 X, 링크만**: "X 정책은 [Decision Y]" 한 줄
- **서비스별 분기 위임**: 상위 concept 에 모든 서비스 분기 나열 X — 서비스 concept 으로 위임 ("서비스마다 다름. {svc} 는 [[integration-{name}]] 참고")
- **중복 작성 방지**: 같은 정책이 여러 concept 에 반복 X — 단일 source ("X 의 Y 는 [[A]] 참고")
- **줄 수 상한 없음**: 도메인 본질이 큰 경우 자연스럽게 길어질 수 있음. 다만 **verbose · 구현 디테일 · 중복**의 결과로 길어진 게 아닌지 점검

**표·다이어그램 사용 시점**:

- **도메인 분류 표** (ex: 사이트 상태 5분류): 도메인 어휘 컬럼만 — UI 표기·카피 컬럼 금지
- **ASCII 플로우 다이어그램**: 프로세스성 concept 의 본질 흐름이 bullet 으로 표현되지 않을 때만. 첫 시도는 bullet
- **에지 케이스 표**: 도메인 차원 처리 (ex: "권한 회수 → 상태 격상") 만. UI 동작 카탈로그 X. 미정 항목은 "미정" 섹션으로

**좋은 예 vs 나쁜 예**:

🚫 나쁜 예 — UI 위치 인용 + 카탈로그:
```
연결 상태는 LNB 의 서비스 아이템 우측 배지, 페이지 리스트 상단 Callout,
헤더 CTA 배지에 동시 표현된다.

| 분류 | LNB 배지 | Callout 메시지 |
| connected | 연결됨 | (없음) |
| expired | 인증 만료 | "재연결이 필요해요" |
```

✅ 좋은 예 — 도메인 어휘:
```
연결 상태는 3분류이며 **단일 source** 로 모든 노출 진입점이 동일
분류로 표현된다 ([Decision X]).

| 분류 | 의미 |
| connected | 토큰 유효 + 권한 정상 |
| expired | 토큰 만료 — 재연결 필요 |
```

🚫 나쁜 예 — CTA 카피 + ASCII 플로우:
```
[1차 모달] → [연동하기] → OAuth → [2차 모달]
                                  ├── [확인] → 확정
                                  └── [취소] → 롤백
```

✅ 좋은 예 — 단계 bullet (도메인 사건):
```
- 최초 연동: OAuth → Admin 판정 → 사용자 확정 시점에 connection 생성
- 수정 시나리오: OAuth → OAuth 복귀 시점에 확정 (토큰 즉시 교체)
```

저장: `~/Projects/flex/til/spec/{feature-name}/` (프로젝트 루트 기준).

### 7. 최종 확인

경로 안내 · Concept별 핵심 요약 · 추가 인터뷰 필요 여부 · 다음 단계(`/drill:prepare`) 안내.

## 완료 판단

핵심 도메인 개념 식별 · 각 Concept 개요·책임·에지 정의 · Concept 간 관계 파악 · 중요한 미결 질문 없음.

## 제약

- 한국어
- 개념 중심 ("어떻게 만들 것인가" 아니라 "어떻게 동작해야 하는가")
- 답변에 따라 자연스러운 follow-up, 질문 방향 유연 조정

## 에러

- 답변 모름 → 대안 제시·함께 고민
- 범위 과대 → 우선순위 조정·Concept 분리
- Linear/Notion/Figma 접근 실패 → 텍스트 기반 진행
