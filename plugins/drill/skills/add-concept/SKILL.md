---
name: add-concept
description: 기존 Spec에 새로운 Concept을 추가합니다
disable-model-invocation: true
argument-hint: "[feature-name] [concept-name|주제-텍스트|linear-url|notion-url|figma-url]"
---

# Add Concept

기존 Spec에 새로운 Concept을 추가합니다.
`plan` 이후 개발 중 새로운 동작 단위가 필요해졌을 때, 전체 plan을 다시 하지 않고 Concept만 독립적으로 추가할 수 있습니다.

## 출력 구조

```
~/Projects/flex/til/spec/{feature-name}/
├── {FEATURE-NAME}.md         # Concepts 테이블에 새 행 추가
└── concepts/
    ├── (기존 concepts...)
    └── {new-concept}.md      # 새로 생성
```

## Workflow

### Phase 1: Feature 식별

- 첫 번째 인자에서 feature name 파싱
- `~/Projects/flex/til/spec/{feature}/` 디렉토리 존재 확인
- Spec index 파일 (`{FEATURE-NAME}.md`) 로드
- 기존 `concepts/*.md` 파일 목록 + 내용 로드 (관계 파악용)
- feature name이 없거나 디렉토리가 없으면 AskUserQuestion으로 요청

### Phase 2: 새 Concept 주제 수집

- 두 번째 인자에서 concept name 또는 주제 텍스트/URL 파싱
- Linear URL → `mcp__linear-server__get_issue`로 이슈 상세 로드
- Notion URL → `mcp__notion__notion-fetch`로 문서 로드
- Figma URL → `mcp__figma__get_design_context`로 디자인 로드
- 주제가 불명확하면 AskUserQuestion으로 명확히 함
- 기존 Concept과 중복되는지 확인 — 중복이면 사용자에게 알리고 기존 Concept 수정을 제안

### Phase 3: 개념 인터뷰

**목표**: `templates/CONCEPT.md`의 각 섹션(개요 / 책임 / 에지 케이스 / 관련 Concept)을 채울 수 있는 수준으로 이 concept이 **무엇인지, 무엇을 책임지는지, 다른 concept과 어떻게 다른지**를 파악한다.

**질문 축 (CONCEPT 섹션 대응):**

| 축 | 대응 섹션 | 샘플 질문 |
|----|-----------|-----------|
| **정체성** | 개요 | "이 개념을 한 문장으로 뭐라고 정의하나요?", "왜 별도 concept인가요? 기존 것에 흡수하면 안 되는 이유는?", "유사한 concept과 결정적으로 다른 점은?" |
| **책임 영역·경계** | 책임 | "이 concept이 담당하는 것은?", "이 concept이 담당하지 않는 것(경계)은?" |
| **동작/플로우** | 책임 — 사용자 플로우 | "사용자가 이 개념을 어떻게 경험하나요? 시작/분기/완료는?" — **프로세스성 concept에만 해당** |
| **규칙·불변** | 책임 — 규칙 | "이 개념의 핵심 규칙·제약은?", "성립해야 할 불변 조건은?" — **모델/구조/정책 concept에 해당** |
| **경계 상황** | 에지 케이스 | "비어있음 / 최초 진입 / 삭제 / 만료 등 상황은?", "예외 상황에서 기대 동작은?" |
| **관계** | 관련 Concept | "어떤 concept에 의존/참조하나요?", "어떤 concept에 영향을 주나요?", "어떤 concept과 혼동되기 쉽지만 다른가요?" |

**질문 가이드라인:**
- **구현 상세 금지**: 로딩 UI / 애니메이션 / 에러 패널 디자인 / 데이터 포맷 / 파일명 / 컴포넌트명 / 라이브러리 선택 등은 묻지 않음 — 이는 티켓·구현 영역
- concept의 "개념성"에 초점: **무엇인가 / 어디까지 책임지나 / 다른 것과 어떻게 다른가**
- 모든 축을 기계적으로 전부 묻지 않음 — concept 유형(모델/구조/프로세스/정책)에 맞는 축을 선택
- 기존 concepts의 책임·에지 케이스를 참조해 경계 질문을 생성
- AskUserQuestion 사용, 한국어

**인터뷰 완료 판단:**
- 한 문장 정의가 섭니다
- 책임 영역 + 경계가 명확함
- 관련 concept과의 차이·관계가 파악됨
- 주요 에지 케이스가 수집됨

### Phase 4: Concept 문서 작성

`templates/CONCEPT.md` 형식으로 `concepts/{name}.md` 생성. 인터뷰 답변을 섹션에 직접 매핑:

| 템플릿 섹션 | 채울 내용 |
|-------------|-----------|
| **개요** | 정체성 답변 — 한 문장 정의 + 별도 존재 이유 |
| **책임** | 책임 영역 + (프로세스성) 사용자 플로우(ASCII 다이어그램) + (모델/구조/정책성) 규칙·불변 |
| **에지 케이스** | 표 형식 — 상황 / 기대 동작 |
| **관련 Concept** | 의존·영향·구분 concept 링크 + 관계 설명 |

**문서 작성 원칙:**
- **개념 명세만 포함**: 정체성·책임·규칙·플로우(해당 시)·에지 케이스·관계
- **구현 상세 제외**: 파일 경로, 코드 스니펫, 함수명, 컴포넌트명, 라이브러리, UI 디테일 등
- 다른 concept에 영향을 주는 부분은 본문에 `[[concept]]` 인라인 링크
- 사용자 플로우는 ASCII 다이어그램으로 표현 (프로세스성 concept만)

작성 후 사용자에게 핵심 책임·에지 케이스 요약을 제시하고 확인을 요청합니다.

### Phase 5: Spec Index 업데이트 + 완료

1. `{FEATURE-NAME}.md`의 **Concepts 테이블**에 새 행 추가
2. 기존 Concept 파일 중 관련 있는 것의 **관련 Concept** 섹션에 새 Concept 링크 추가
3. `.drill-state.json`은 건드리지 않음 (add-concept은 독립 보조 스킬)

**완료 안내:**
- 생성된 파일 경로
- 핵심 책임·에지 케이스 요약
- 업데이트된 기존 파일 목록
- 다음 단계 안내: 필요시 `/drill:prepare`로 관련 티켓 생성

## 중요 사항

- **언어**: 모든 질문과 커뮤니케이션은 한국어
- **동작 중심**: 구현이 아닌 동작에 집중
- **코드 수정 금지**: spec/concept 파일만 수정
- **확인**: 파일 작성 전 반드시 사용자 확인
- **독립 실행**: drill 오케스트레이터 없이 단독 실행 가능
- **중복 방지**: 기존 Concept과 중복 시 수정을 제안

## 에러 처리

- Feature 디렉토리 없음: AskUserQuestion으로 feature name 재확인, 또는 `/drill:plan`으로 Spec 먼저 생성 안내
- 기존 Concept과 중복: 기존 Concept 수정을 제안하고, 사용자가 별도 Concept을 원하면 진행
- Linear/Notion/Figma 접근 실패: 텍스트 기반으로 진행
