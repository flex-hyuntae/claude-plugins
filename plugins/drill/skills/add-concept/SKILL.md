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

### Phase 3: 동작 인터뷰

**목표**: 새 Concept의 구체적인 동작, UX 플로우, 에지 케이스를 파악한다.

**질문 카테고리:**
- **사용자 플로우**: 시작점, 분기, 완료 조건, 취소/되돌리기
- **에지 케이스**: 예외 상황, 경계 조건, 동시성, 빈 상태
- **인터랙션 디테일**: 로딩, 에러 표시, 성공 피드백, 애니메이션
- **데이터 제약**: 최대/최소값, 필수/선택, 형식 제한
- **권한/조건**: 접근 권한, feature flag, 사전 조건
- **기존 Concept 관계**: 이 Concept이 하지 않는 것, 다른 Concept이 담당하는 경계

**질문 가이드라인:**
- 명백하거나 피상적인 질문 금지
- 구현 상세(파일명, 함수명, 라이브러리)가 아닌 **동작**에 집중
- "만약 ~한 상황이라면?" 형태의 시나리오 기반 질문
- 기존 Concept의 SHOULD/SHOULD NOT을 참조하여 경계 질문 생성
- AskUserQuestion 사용, 한국어

**인터뷰 완료 판단:**
- SHOULD/SHOULD NOT이 정의됨
- 주요 사용자 플로우가 파악됨
- 에지 케이스가 충분히 수집됨
- 기존 Concept과의 경계가 명확함

### Phase 4: Concept 문서 작성

`templates/CONCEPT.md` 형식으로 `concepts/{name}.md` 생성:
- 이 동작이 해결하는 문제
- SHOULD: 기본 동작, 사용자 플로우 (ASCII 다이어그램), 에지 케이스
- SHOULD NOT: 금지 동작 + 담당 Concept
- 관련 Concept 링크

**문서 작성 원칙:**
- **동작 명세만 포함**: 사용자 플로우, 에지 케이스, SHOULD/SHOULD NOT
- **구현 상세 제외**: 파일 경로, 코드 스니펫, 함수명, 컴포넌트명 등
- 사용자 플로우는 ASCII 다이어그램으로 표현

작성 후 사용자에게 핵심 SHOULD/SHOULD NOT 요약을 제시하고 확인을 요청합니다.

### Phase 5: Spec Index 업데이트 + 완료

1. `{FEATURE-NAME}.md`의 **Concepts 테이블**에 새 행 추가
2. 기존 Concept 파일 중 관련 있는 것의 **관련 Concept** 섹션에 새 Concept 링크 추가
3. `.drill-state.json`은 건드리지 않음 (add-concept은 독립 보조 스킬)

**완료 안내:**
- 생성된 파일 경로
- 핵심 SHOULD/SHOULD NOT 요약
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
