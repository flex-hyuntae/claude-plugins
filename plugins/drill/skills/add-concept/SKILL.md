---
name: add-concept
description: 기존 Spec에 새로운 Concept을 추가합니다
disable-model-invocation: true
argument-hint: "[feature-name] [concept-name|주제-텍스트|linear-url|notion-url|figma-url]"
---

# Add Concept

기존 Spec에 Concept만 독립적으로 추가. 전체 plan을 다시 하지 않고 개발 중 새로운 동작 단위만 확장.

## Workflow

### 1. Feature 식별

- 인자 1에서 feature name 파싱 → `~/Projects/flex/til/spec/{feature}/` 존재 확인
- Spec index + 기존 `concepts/*.md` 로드 (관계 파악용)
- 없으면 AskUserQuestion 또는 `/drill:plan` 안내

### 2. 새 Concept 주제 수집

- 인자 2 해석 — concept name / 텍스트 / Linear·Notion·Figma URL
- URL이면 각 MCP로 로드 (`get_issue`, `notion-fetch`, `get_design_context`)
- 기존 Concept과 중복 의심 → 중복 알림 + 기존 Concept 수정 제안

### 3. 개념 인터뷰

목표: `templates/CONCEPT.md` 섹션(개요·책임·에지 케이스·관련 Concept)을 채울 수준. 한국어 AskUserQuestion.

**질문 축:**

| 축 | 대응 섹션 | 예시 |
|----|-----------|------|
| 정체성 | 개요 | "한 문장 정의?", "왜 별도 concept?" |
| 책임·경계 | 책임 | "담당 / 담당 않는 것?" |
| 동작/플로우 | 책임 (프로세스성) | "시작·분기·완료?" |
| 규칙·불변 | 책임 (모델/구조/정책성) | "핵심 규칙·불변?" |
| 경계 상황 | 에지 케이스 | "빈/예외/만료/삭제?" |
| 관계 | 관련 Concept | "의존·영향·구분되는 concept?" |

concept 유형(모델/구조/프로세스/정책)에 맞는 축만 선택. **구현 상세는 묻지 않음** (UI·파일명·라이브러리 등은 티켓 영역).

완료 조건: 한 문장 정의 · 책임·경계 명확 · 관련 concept 관계 파악 · 주요 에지 케이스 수집.

### 4. Concept 문서 작성

`concepts/{name}.md` 생성 (`templates/CONCEPT.md` 기반). 인터뷰 답변을 섹션에 매핑:

- **개요**: 한 문장 정의 + 별도 존재 이유
- **책임**: 책임 영역 + (프로세스성) ASCII 플로우 / (모델성) 규칙·불변
- **에지 케이스**: 상황 / 기대 동작 표
- **관련 Concept**: 의존·영향·구분 concept 링크

다른 concept에 영향 주는 부분은 `[[concept]]` 인라인 링크. **구현 상세 제외**.

작성 후 핵심 책임·에지 케이스 요약 제시 + 사용자 확인.

### 5. Spec Index 업데이트 + 완료

1. `{FEATURE-NAME}.md` Concepts 테이블에 새 행 추가
2. 관련 기존 Concept의 "관련 Concept" 섹션에 새 링크 추가
3. `.drill-state.json` 은 건드리지 않음 (보조 스킬)

완료 안내: 생성 파일 경로, 책임·에지 케이스 요약, 수정된 기존 파일, 필요시 `/drill:prepare` 안내.

## 제약

- 한국어, 동작 중심, spec/concept 파일만 수정
- 파일 작성 전 사용자 확인
- 기존 Concept과 중복 시 수정 우선 제안

## 에러

- Feature 디렉토리 없음 → `/drill:plan` 안내
- Linear/Notion/Figma 접근 실패 → 텍스트 기반 진행
