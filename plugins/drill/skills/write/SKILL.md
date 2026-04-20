---
name: write
description: Linear 티켓을 받아 Spec/Concept 기반으로 코드를 작성합니다
disable-model-invocation: true
argument-hint: "[linear-issue-url|issue-id]"
---

# Write

Linear 티켓 하나를 받아 Spec/Concept + 구현 가이드로 코드 작성. rules 규칙은 `rules:write` 스킬이 자동 적용 (rules 플러그인 필요).

## Workflow

### 1. 컨텍스트 로드

1. `mcp__linear-server__get_issue` 로 티켓
2. description에서 관련 Concept 경로 추출 → Spec index + Concept 파일 로드
3. 확인: 목표 / 수용 기준 / 구현 가이드 / 코드 위치

### 2. 코드베이스 탐색 (인터랙티브)

Glob/Grep으로 관련 파일 → 핵심 파일 Read → 기존 패턴·유틸 재사용 판단.

적절한 위치를 찾을 때까지 AskUserQuestion 반복:
- 컴포넌트/로직/타입 추가 위치
- 기존 재사용 vs 신규 생성

### 3. 코드 작성 (반복)

수용 기준을 하나씩 충족:
1. Concept 책임·에지 케이스 = 수용 기준
2. 구현 가이드 방향에 맞게 Edit/Write
3. `rules:write` 자동 적용 (직접 로드 안 함)

**작업 단위 완료 후 AskUserQuestion**: "커밋 / 이어서 진행".

### 4. 검증

```bash
yarn turbo run type-check --filter=@flex-apps/{pkg}
yarn turbo run lint --filter=@flex-apps/{pkg}
```

에러 수정 후 재검증.

### 5. 완료

변경 파일 목록 + 수용 기준 충족 체크리스트. drill state 업데이트 (오케스트레이션 시).

## 제약

- 한 번에 티켓 1개만
- 한국어, 코드 위치·커밋 지속 확인

## 에러

- 티켓 조회 실패 → URL/ID 재확인
- Spec/Concept 없음 → 티켓 정보만으로 진행 또는 `/drill:plan` 안내
- type-check/lint 실패 → 수정 후 재검증
