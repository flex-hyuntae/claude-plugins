# best-practices

코드 생성 및 리뷰 시 참고할 코딩 컨벤션과 성능 최적화 규칙.

## Structure

```
best-practices/
├── rules/              # 개별 규칙 파일 (source of truth)
│   ├── react/          # React 성능 + 패턴 (24 rules)
│   ├── typescript/     # TypeScript 규칙 (1 rule)
│   └── structure/      # 프로젝트 구조 규칙 (3 rules)
└── skills/             # 카테고리별 quick reference
    ├── react/
    ├── typescript/
    ├── structure/
    └── add-best-practice/
```

## Categories

| Category | Rules | Impact | Description |
|----------|-------|--------|-------------|
| React | 24 | CRITICAL-LOW | 성능 최적화, 상태 관리 패턴 |
| TypeScript | 2 | HIGH | 타입 안전성 규칙 |
| Structure | 3 | MEDIUM-HIGH | 프로젝트 구조, 코드 구성 |

## Skills

| Skill | Description |
|-------|-------------|
| `add-best-practice` | 새 규칙을 rules/에 추가 |
