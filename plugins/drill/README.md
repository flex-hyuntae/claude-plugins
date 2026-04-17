# drill

Spec/Concept 기반 개발 워크플로우 오케스트레이션 플러그인.

인터뷰를 통해 Spec + Concepts를 작성하고, 티켓을 생성하고, 개발 후 Spec과 구현의 차이를 동기화하고, TC를 작성하는 전체 흐름을 관리합니다.

## 워크플로우

```
plan → prepare → write → review → qa
```

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `drill` | 전체 워크플로우 오케스트레이션 (상태 추적, 이어하기) |
| `plan` | 심층 인터뷰 → SPEC.md + Concepts 작성 |
| `add-concept` | 기존 Spec에 새로운 Concept 추가 (독립 실행) |
| `prepare` | Spec/Concepts → Linear 티켓 생성 또는 기존 티켓 강화 |
| `write` | Linear 티켓 기반 Spec/Concept 참조 코드 작성 |
| `review` | PR vs Spec/Concept 차이 감지 → Decision Log 작성 |
| `qa` | Spec + Concepts + Decision Log → TC 작성 |

## 출력 구조

```
~/Projects/flex/til/spec/{feature-name}/
├── {FEATURE-NAME}.md       # Index — 문제 정의, 전체 동작, concept 링크, archived 표기
├── concepts/
│   ├── table.md            # 개별 동작 명세 (SHOULD/SHOULD NOT)
│   ├── error-panel.md
│   └── _archive/
│       └── old-concept.md  # 폐기/대체된 concept. archive 배너 + 결정 근거 링크
├── decisions/
│   └── 2026-03-27-001.md   # Decision log (PR 동기화 + Concept 폐기/대체 포함)
├── TC.md                   # 테스트 케이스
└── .drill-state.json       # 워크플로우 상태
```

## Archive 정책

Concept이 폐기되거나 다른 Concept으로 대체되면 **삭제하지 않고 archive**합니다:

- 위치: `concepts/_archive/{name}.md`
- 파일 상단에 `⚠️ Archived (YYYY-MM-DD)` 배너 + 대체 concept 링크 + decision log 링크
- SPEC.md concepts 테이블에서는 제거하고 테이블 아래 `archived:` 한 줄로 표기
- 폐기 결정은 `decisions/`에 반드시 기록 (`/drill:review`의 "Concept 폐기/대체" 선택지)

## 사용 예시

### 전체 워크플로우
```
/drill:drill job-grade-modal
```

### 개별 스킬
```
/drill:plan 직급 생성 모달
/drill:add-concept job-grade-modal 에러 패널
/drill:prepare job-grade-modal
/drill:write CORE-1234
/drill:review https://github.com/org/repo/pull/123
/drill:qa job-grade-modal
```

### 이어하기
```
/drill:drill resume
```

## 템플릿

`templates/` 디렉토리에 각 문서의 템플릿이 있습니다:
- `SPEC.md` — Index spec 템플릿
- `concept.md` — Concept 템플릿 (SHOULD/SHOULD NOT)
- `decision.md` — Decision Log 템플릿
- `TC.md` — TC 템플릿 (커버리지 매트릭스 포함)
