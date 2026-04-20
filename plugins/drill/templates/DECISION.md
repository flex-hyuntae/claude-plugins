# Decision: {간략 제목}

- **날짜**: YYYY-MM-DD
- **관련 Concept**: [concept-name](../concepts/concept-name.md) (없으면 "해당 없음")
- **관련 티켓**: [FLEX-123](https://linear.app/...) (1개 이상)
- **트리거**: PR #XXX 리뷰 | 로컬 검증 중 | 팀원 리뷰 논의 | 디자인/기획 리뷰 | 스펙 단계 논의 | 기타
- **Cascade 범위**: ticket_only | ticket_concept | ticket_concept_spec

## 결정

[한두 문장으로 정리된 결정 사항]

## 변경 전 (Spec/Concept/Ticket 원문)

[변경되기 전 내용 인용 — 신규 결정이면 "해당 없음"]

## 변경 후 (실제 구현 또는 갱신된 Spec/Ticket)

[구현 / 티켓 / 스펙에서 달라진 점]

## 변경 이유

[왜 달라졌는지 — 사용자 인터뷰 답변을 그대로 반영]

## 영향

- **티켓**: [FLEX-123 description 수정 항목]
- **Concept**: [수정/추가/폐기된 concept 파일] (cascade ≥ ticket_concept)
- **Spec**: [SPEC.md에서 변경된 섹션] (cascade = ticket_concept_spec)
- **기타 파일/티켓**: [영향받는 다른 concept/파일/티켓 나열]

<!--
Concept 폐기/대체 결정일 때:
- 기존 concept은 `concepts/_archive/{name}.md`로 이동
- 이동한 파일 상단에 아래 배너 삽입:
  > **⚠️ Archived (YYYY-MM-DD)**
  > {기존 concept} 개념은 [대체 concept](../{new-concept}.md)으로 대체되었습니다.
  > 결정 근거: ../../decisions/YYYY-MM-DD-NNN.md
- SPEC.md concepts 테이블에서 제거하고 archived 한 줄 추가
- 연결 다이어그램에서 기존 concept 링크 제거
-->
