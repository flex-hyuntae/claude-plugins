# drill

Spec/Concept 기반 개발 워크플로우 오케스트레이션 플러그인.

인터뷰를 통해 Spec + Concepts를 작성하고, 티켓을 생성하고, 개발 후 Spec과 구현의 차이를 동기화하고, TC를 작성하는 전체 흐름을 관리합니다.

## 워크플로우

```
plan → prepare → [개발] → review → qa
```

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `drill` | 전체 워크플로우 오케스트레이션 (상태 추적, 이어하기) |
| `plan` | 심층 인터뷰 → SPEC.md + Concepts 작성 |
| `prepare` | Spec/Concepts → Linear 티켓 생성 또는 기존 티켓 강화 |
| `review` | PR vs Spec/Concept 차이 감지 → Decision Log 작성 |
| `qa` | Spec + Concepts + Decision Log → TC 작성 |

## 출력 구조

```
~/Projects/flex/til/spec/{feature-name}/
├── SPEC.md              # Index — 문제 정의, 전체 동작, concept 링크
├── concepts/
│   ├── table.md         # 개별 동작 명세 (SHOULD/SHOULD NOT)
│   └── error-panel.md
├── decisions/
│   └── 2026-03-27-001.md  # Decision log
├── TC.md                # 테스트 케이스
└── .drill-state.json    # 워크플로우 상태
```

## 사용 예시

### 전체 워크플로우
```
/drill:drill job-grade-modal
```

### 개별 스킬
```
/drill:plan 직급 생성 모달
/drill:prepare job-grade-modal
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
