---
name: review
description: PR과 Spec/Concept을 비교하여 차이를 감지하고 Decision Log를 작성합니다
disable-model-invocation: true
argument-hint: "[feature-name] [pr-url|pr-number]"
---

# Review

PR 생성 후 실제 구현과 Spec/Concept을 비교하여 차이를 감지합니다.
차이가 없으면 없다고 알려주고 끝냅니다.
차이가 있으면 각 차이에 대해 처리 방식을 물어보고, Decision Log 작성 및 Concept 업데이트를 수행합니다.

## Workflow

### Phase 1: PR 로드

**인자 파싱:**
- GitHub PR URL → `gh pr view` 또는 `mcp__github__pull_request_read`로 PR 정보 로드
- PR 번호 → 현재 리포에서 PR 로드
- 인자 없음 → 현재 브랜치의 최신 PR 자동 감지

**수집 정보:**
- PR 제목, 설명
- 변경 파일 목록
- PR diff (`gh pr diff`)

### Phase 2: Spec/Concept 로드

**Feature 식별:**
- 인자로 feature name이 주어지면 그대로 사용
- 없으면 AskUserQuestion으로 feature name 요청

**문서 로드:**
- `~/Projects/flex/til/spec/{feature}/{FEATURE-NAME}.md` 읽기
- `~/Projects/flex/til/spec/{feature}/concepts/*.md` 모두 읽기
- `~/Projects/flex/til/spec/{feature}/decisions/*.md` 기존 Decision Log 읽기 (있으면)

스펙이 없으면: "연결할 Spec이 없습니다. `/drill:plan`으로 먼저 Spec을 작성하거나, 이 PR은 Spec 없이 진행하시겠습니까?"

### Phase 3: 차이 감지

PR diff와 각 Concept의 SHOULD/SHOULD NOT을 의미적으로 비교합니다.
diff만으로 판단이 어려운 부분은 AskUserQuestion으로 사용자에게 질문하여 확인합니다.

**확인 질문 예시:**
- "Concept '{name}'에 '{SHOULD 항목}'이 정의되어 있는데, PR diff에서 관련 구현을 찾지 못했습니다. 이 동작이 이 PR에 포함되어 있나요?"
- "이 PR에서 '{구현 내용}'이 추가된 것 같은데, 기존 Concept에 없는 동작입니다. 맞나요?"

**차이가 없으면:**
"Spec과 구현이 일치합니다." 로 종료합니다. 억지로 차이를 찾지 않습니다.

**차이가 있으면:**
각 차이를 Phase 4에서 하나씩 처리합니다.

**감지 유형:**

| 유형 | 설명 |
|------|------|
| **SHOULD 미구현** | Concept에 정의된 동작이 구현되지 않음 |
| **동작 변경** | 에지 케이스 처리 등이 Concept과 다름 |
| **신규 동작 추가** | Concept에 없는 동작이 구현됨 |

### Phase 4: 차이 인터뷰

각 감지된 차이에 대해 하나씩 질문합니다.
AskUserQuestion 사용, 한국어.

**질문 패턴:**

```
Concept '{name}'에서는 "{SHOULD 항목}"으로 정의되어 있는데,
실제 구현에서는 "{구현 내용}"으로 되어 있습니다.
이 차이는 어떻게 처리할까요?
```

**선택지:**
- **의도적 변경** — Decision Log 생성 + 기존 Concept 업데이트
- **Concept 추가 필요** — 새 Concept 파일 생성 + Decision Log
- **Concept 폐기/대체** — 기존 Concept을 `_archive/`로 이동 + Decision Log
- **구현 누락** — Linear 티켓 생성 (추후 수정 대상)
- **다른 작업에서 구현 예정** — 이 PR 범위가 아님, 기존 또는 별도 티켓에서 처리
- **건너뛰기** — 이 차이는 무시

### Phase 5: 처리 실행

각 선택에 따라 실행합니다:

**의도적 변경:**
1. `~/Projects/flex/til/spec/{feature}/decisions/YYYY-MM-DD-NNN.md` Decision Log 작성 (`templates/DECISION.md` 참조)
2. 해당 Concept의 SHOULD/SHOULD NOT 항목 수정
3. Spec 파일 Decision Log 테이블에 항목 추가

**Concept 추가 필요:**
1. Decision Log 작성
2. `~/Projects/flex/til/spec/{feature}/concepts/{new-name}.md` 새 Concept 파일 생성 (`templates/CONCEPT.md` 참조)
3. Spec 파일 Concepts 테이블 + Decision Log 테이블 업데이트

**Concept 폐기/대체:**
1. `~/Projects/flex/til/spec/{feature}/decisions/YYYY-MM-DD-slug.md` Decision Log 작성
   - "트리거"에 PR 또는 스펙 논의 명시
   - 대체 concept이 있으면 링크
2. 기존 Concept 파일을 `concepts/_archive/{name}.md`로 이동 (디렉토리 없으면 생성)
3. 이동한 파일 상단에 archive 배너 추가:
   ```
   > **⚠️ Archived (YYYY-MM-DD)**
   > {concept-name} 개념은 [{대체 concept}](../{new}.md)으로 대체되었습니다.
   > 결정 근거: ../../decisions/YYYY-MM-DD-slug.md
   ```
4. Spec 파일 업데이트:
   - Concepts 테이블에서 해당 행 제거
   - 테이블 아래에 `archived: [name](concepts/_archive/name.md) — [사유 또는 대체] (YYYY-MM-DD)` 한 줄 추가
   - Concept 연결 리스트에서 해당 concept 링크 제거
   - Decision Log 테이블에 항목 추가
5. 다른 Concept 파일들의 "관련 Concept" / 인라인 `[[name]]` 참조 정리

**구현 누락:**
1. Linear 티켓 생성 (`mcp__linear-server__save_issue`)
   - 제목: 누락된 SHOULD 항목 기반
   - 관련 Concept 경로 포함: `~/Projects/flex/til/spec/{feature}/concepts/{name}.md`
2. 사용자에게 생성된 티켓 URL 안내

**다른 작업에서 구현 예정:**
- 아무것도 하지 않음 (이미 다른 티켓/PR에서 다룰 예정)

**건너뛰기:**
- 아무것도 하지 않음

### Phase 6: 완료 안내

처리 결과를 간단히 안내합니다:
- 업데이트된 파일 목록
- 생성된 Decision Log
- 생성된 Linear 티켓 (구현 누락 건)

## 중요 사항

- **언어**: 모든 커뮤니케이션은 한국어
- **코드 수정 금지**: spec/concept/decision 파일만 수정. 소스 코드 수정 안 함
- **억지로 찾지 않음**: 차이가 없으면 없다고 하고 끝냄
- **확인**: 파일 수정 전 반드시 사용자 확인

## 에러 처리

- PR 조회 실패: PR URL/번호 재확인 요청
- Spec 없음: Spec 없이 진행하거나 `/drill:plan` 안내
- Linear 티켓 생성 실패: 에러 메시지 표시, 수동 생성 안내
