# drill

Spec/Concept 기반 개발 워크플로우 오케스트레이션 플러그인.

인터뷰를 통해 Spec + Concepts를 작성하고, 티켓을 생성하고, 개발 후 Spec과 구현의 차이를 동기화하고, TC를 작성하는 전체 흐름을 관리합니다.

## 워크플로우

```
plan → prepare → write | ship → review → qa
```

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `drill` | 전체 워크플로우 오케스트레이션 (상태 추적, 이어하기) |
| `plan` | 심층 인터뷰 → SPEC.md + Concepts 작성 |
| `add-concept` | 기존 Spec에 새로운 Concept 추가 (독립 실행) |
| `prepare` | Spec/Concepts → Linear 티켓 생성 또는 기존 티켓 강화 |
| `write` | Linear 티켓 1개 기반 코드 작성 |
| `ship` | 티켓 N개 → 의존 그래프 → worktree + batch draft PR (write 를 감쌈) |
| `review` | PR vs Spec/Concept 차이 감지 → Decision Log 작성 |
| `qa` | Spec + Concepts + Decision Log → TC 작성 |

## 출력 구조

```
~/Projects/flex/wiki/Spec/{feature-name}/
├── {FEATURE-NAME}.md       # Index — 문제 정의, 전체 동작, concept 링크, archived 표기
├── concepts/
│   ├── table.md            # 개별 동작 명세 (책임 / 에지 케이스)
│   ├── error-panel.md
│   └── _archive/
│       └── old-concept.md  # 폐기/대체된 concept. archive 배너 + 결정 근거 링크
├── decisions/
│   └── 2026-03-27-001.md   # Decision log (PR 동기화 + Concept 폐기/대체 포함)
├── TC.md                   # 테스트 케이스
└── .drill-state.json       # 워크플로우 상태
```

## 공용 참조

스킬·에이전트가 공유하는 단일 출처. 규칙을 고칠 때는 여기만 고칩니다.

| 파일 | 역할 |
|------|------|
| `references/CONCEPT-WRITING.md` | spec/concept 어휘의 단일 출처 — KEEP/DROP 카탈로그, 좋은/나쁜 예, 분리vs통합 |
| `references/STACK.md` | FE / BE 가 갈리는 지점만 — stack 감지, 검증 커맨드, 의존 방향, QA 검증 지점, BE 컨벤션 위임 |

## 티켓 분해 · Archive

- 티켓 3방향 분해([플로우]/[마크업]/[API])와 의존 규칙 → `skills/prepare/SKILL.md` §3
- BE 는 3축에 억지로 맞추지 않습니다 — `[플로우]` 만 공용, 그 외는 prefix 없이 (`references/STACK.md`)
- Concept 폐기 시 삭제하지 않고 `concepts/_archive/` 로 archive + decision log 기록 → `skills/review/SKILL.md` §6

## BE 지원

drill 은 BE 컨벤션을 직접 갖지 않습니다. 절차·게이트·문서 형식은 stack 공용이고, BE 규칙 본문은 `backend-guidelines` 플러그인의 `doc-loader` 에이전트에 위임합니다 (미설치면 생략하고 진행).

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
/drill:ship CORE-1234 CORE-1235 CORE-1236
/drill:review https://github.com/org/repo/pull/123
/drill:qa job-grade-modal
/drill:drill resume
```

## 템플릿

`templates/` — `SPEC.md` (Index) · `CONCEPT.md` (책임/에지) · `DECISION.md` · `TC.md` (커버리지 매트릭스 포함)
