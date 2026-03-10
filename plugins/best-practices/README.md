# best-practices

코드 생성 및 리뷰 시 참고할 코딩 컨벤션과 성능 최적화 규칙.

## Structure

```
best-practices/
├── rules/              # 개별 규칙 파일 (source of truth)
│   ├── react/          # React 성능 + 패턴 (24 rules)
│   ├── typescript/     # TypeScript 규칙 (3 rules)
│   ├── structure/      # 프로젝트 구조 규칙 (3 rules)
│   ├── styling/        # CSS/vanilla-extract 규칙 (2 rules)
│   ├── accessibility/  # 접근성 규칙 (1 rule)
│   ├── testing/        # 테스트 품질 규칙 (1 rule)
│   └── naming/         # 네이밍/문서화/i18n 규칙 (1 rule)
└── skills/             # 카테고리별 quick reference
    ├── react/
    ├── typescript/
    ├── structure/
    ├── styling/
    ├── accessibility/
    ├── testing/
    ├── naming/
    └── add-best-practice/
```

## Categories

| Category | Rules | Impact | Description |
|----------|-------|--------|-------------|
| React | 24 | CRITICAL-LOW | 성능 최적화, 상태 관리 패턴 |
| TypeScript | 3 | HIGH | 타입 안전성 규칙 |
| Structure | 3 | MEDIUM-HIGH | 프로젝트 구조, 코드 구성 |
| Styling | 2 | HIGH | vanilla-extract 패턴, 디자인 토큰 |
| Accessibility | 1 | HIGH | 시맨틱 HTML, ARIA, 키보드 |
| Testing | 1 | MEDIUM | AAA 패턴, 동작 기반 테스트 |
| Naming | 1 | MEDIUM | 네이밍 컨벤션, i18n, 주석 |

## Skills

| Skill | Description |
|-------|-------------|
| `add-best-practice` | 새 규칙을 rules/에 추가 |
