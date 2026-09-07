# Codex 하위 에이전트 위임

이 플러그인의 `drill-*` 분석 역할은 Claude의 고정 Agent 정의가 아니다. 각 역할 문서는 **Codex 하위 에이전트에 줄 역할 프롬프트**다.

## 호출 규칙

1. 해당 역할 문서를 읽고, 그 문서의 입력 계약과 현재 작업 입력을 함께 전달해 Codex 하위 에이전트를 시작한다.
2. 역할 문서의 읽기 전용 경계를 유지한다. 분석 역할은 파일·티켓·PR을 수정하거나 사용자에게 직접 질문하지 않는다.
3. 반환값은 역할 문서의 출력 형식으로 압축한다. 원본 본문과 대량 로그를 메인 컨텍스트에 복사하지 않는다.
4. 하위 에이전트를 사용할 수 없는 실행 환경이면, 같은 역할 문서를 읽고 메인에서 동일한 읽기 전용 분석을 수행한다. 병렬 실행을 했다고 말하지 않는다.

## 역할 문서

| 역할 | 참조 |
| --- | --- |
| 소스 요약 | `references/agents/drill-plan-source.md` |
| 코드 후보 탐색 | `references/agents/drill-code-explore.md` |
| 구현 설계 | `references/agents/drill-design.md` |
| 의존 그래프 | `references/agents/drill-deps.md` |
| PR·티켓 차이 분석 | `references/agents/drill-review.md` |
| QA TC 초안 | `references/agents/drill-qa.md` |
