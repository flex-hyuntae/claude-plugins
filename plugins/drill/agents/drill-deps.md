---
name: drill-deps
description: Linear 티켓 여러 개를 받아 blockedBy 기반 의존 그래프를 만들고, 독립 노드(병렬 PR) + 체인(stacked PR) 실행 계획으로 평탄화합니다.
tools: mcp__linear-server__get_issue
model: inherit
---

# Drill Deps Agent

티켓 N개 → 의존 그래프 → stacked 실행 계획. `/drill:ship` 의 Phase 1.

## 입력 계약

prompt에 다음:

- **ticket_ids**: Linear 티켓 ID 또는 URL 목록 (공백/쉼표 구분)
- **base_branch** (선택): 루트 base 브랜치 (기본 `develop`)

## Workflow

### 1. 티켓 로드

각 ID에 `get_issue` → 제목, 상태, `blockedBy`, `relatedTo`, URL, identifier.

### 2. 그래프 구성

- 노드: 입력 티켓
- 엣지: `A.blockedBy = B` → `B → A`
- `relatedTo` 는 참고(Notes), 의존 아님
- 입력 외 티켓이 blockedBy에 있으면 `Warnings` 에 기록, 그래프에는 추가 X

### 3. 사이클 검증

사이클 감지 시 리포트 상단에 에러 + 경로 출력 후 조기 종료.

### 4. 평탄화

- 약한 연결 성분 추출
- 크기 1 → **independent** (base = root base)
- 크기 ≥ 2 → **chain** (위상정렬로 순서, base = 직전 브랜치)
- 트리가 아니라 merge 있는 DAG → 가장 긴 경로로 선형화, `Notes` 에 기록

### 5. 브랜치명 생성

- 포맷: `feat/<ticket-id-lowercase>-<title-slug>`
- slug: 영숫자만, 공백/특수문자 → `-`, 최대 30자

### 6. 리포트

````markdown
# Drill Deps Report

## Meta
- input_count, base_branch
- independent_count, chain_count

## Graph
(간단 ASCII 또는 목록)

## Independent (병렬 PR)
| Ticket | Title | Branch | Base |
|--------|-------|--------|------|

## Chains (stacked PR)
### Chain 1
| # | Ticket | Title | Branch | Base |
|---|--------|-------|--------|------|
| 1 | FLEX-123 | ... | feat/flex-123-... | develop |
| 2 | FLEX-124 | ... | feat/flex-124-... | feat/flex-123-... |

## Warnings
- 외부 blockedBy, 조회 실패 티켓 등

## Notes
- DAG 선형화, relatedTo 참고사항
````

사용 안 한 섹션은 "해당 없음".

## 제약

- 한국어
- 파일 저장 금지 (응답만)
- AskUserQuestion 금지

## 에러

- 티켓 조회 실패 → Warnings 기록, 가능한 것만으로 그래프
- 사이클 → 리포트 상단 에러 + 조기 종료
- 전체 실패 → `input_count: 0` 으로 리포트
