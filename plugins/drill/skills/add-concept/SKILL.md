---
name: add-concept
description: '기존 Spec에 새로운 Concept만 독립적으로 추가한다. 사용자가 "/drill:add-concept", "concept 추가", "새 개념 정의", "스펙에 도메인 추가"를 요청할 때 트리거. 전체 plan 인터뷰를 다시 하지 않고, 개발 중 발견한 새 동작 단위만 확장할 때 사용. plan과 동일한 작성 원칙(도메인 어휘·구현 디테일 금지·what/why 만) 적용.'
compatibility: 'Linear/Notion/Figma MCP 권장 (URL 입력 시).'
disable-model-invocation: true
argument-hint: "[feature-name] [concept-name|주제-텍스트|linear-url|notion-url|figma-url]"
---

# Add Concept

기존 Spec에 Concept만 독립적으로 추가. 전체 plan을 다시 하지 않고 개발 중 새로운 동작 단위만 확장.

> **본질·원칙·인터뷰 방법은 `plan` skill 과 동일** — 본 문서는 add-concept 특이 사항만 다룬다. 동일 항목은 plan 참조.

## Workflow

### 1. Feature 식별

- 인자 1에서 feature name 파싱 → `~/Projects/flex/til/spec/{feature}/` 존재 확인
- Spec index + 기존 `concepts/*.md` 로드 (관계 파악용)
- 없으면 AskUserQuestion 또는 `/drill:plan` 안내

### 2. 새 Concept 주제 수집

- 인자 2 해석 — concept name / 텍스트 / Linear·Notion·Figma URL
- URL이면 각 MCP로 로드 (`get_issue`, `notion-fetch`, `get_design_context`)
- **기존 Concept과 중복 의심 → 중복 알림 + 기존 Concept 수정 제안** (add-concept 만의 단계)

### 3. 개념 인터뷰

목표: `templates/CONCEPT.md` 섹션(개요·책임·관련 Concept·관련 Decision·미정)을 채울 수준. 한국어 AskUserQuestion.

plan `§3 도메인 심층 인터뷰` 그대로. add-concept 만의 차이:

- 한 Concept 범위 — 새로 추가하는 1개만 인터뷰 (plan 처럼 여러 Concept 분해 단계 없음)
- 기존 Concept 들과의 관계 질문을 추가로 — "기존 [[A]] 와 어떻게 구분되는가?" / "[[B]] 가 본 concept 을 어떻게 참조해야 하는가?"

### 4. Concept 문서 작성

`concepts/{name}.md` 생성 (`templates/CONCEPT.md` 기반). 인터뷰 답변을 섹션에 매핑.

**작성 원칙은 `plan` skill `§6 문서 작성` + `references/CONCEPT-WRITING.md` 와 동일.** 문서 구조:

- **목차**: H1 (`# Concept: {Name}`) 다음에 ToC 블록 (`minLevel: 2 / maxLevel: 4 / exclude: /^목차$/`, language `toc`)
- **개요·책임·관련 Concept·관련 Decision·미정** 섹션 순
- **§관련 Decision**: 본 concept 영향 decision 들을 표(날짜·요약·영향 부분) 로 모음. 본문 인라인 `[Decision X](path)` 금지

작성 후 `references/CONCEPT-WRITING.md` 자가 점검 키워드로 매체·구현·how 어휘 누출 점검.

**책임 단위 분리 모호 시 AskUserQuestion** — 어떤 동작을 본 concept 안에 두는가, 별도 concept 으로 빼는가가 애매하면 추정으로 진행하지 말고 사용자 결정을 받는다.

**결정은 항상 decision log 로 남긴다** — 임시·잠정 결정도 추적성을 위해 decision log 발급. 미확정 부분은 concept "미정" 섹션에 표기 (둘은 병행).

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
