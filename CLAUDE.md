# Claude Code 프로젝트 지침

## 플러그인 버전 관리 규칙

`plugins/<name>/` 하위 파일을 수정·추가·삭제할 때 (README.md 제외) **반드시** 버전을 올린다.

### 업데이트 대상 (두 곳 동시)

1. `plugins/<name>/.claude-plugin/plugin.json` → `version`
2. `.claude-plugin/marketplace.json` → 해당 플러그인의 `version`

두 값은 항상 동일해야 한다.

### 버전 결정 로직

형식: `YYYY.MM[.patch]` — 현재 날짜 기준으로 판단한다.

| 기존 버전 | 조건 | 새 버전 |
|-----------|------|---------|
| 이번 달이 아닌 경우 | — | `YYYY.MM` |
| `YYYY.MM` | 이번 달과 동일 | `YYYY.MM.1` |
| `YYYY.MM.N` | 이번 달과 동일 | `YYYY.MM.(N+1)` |

### 커밋 전 체크리스트

플러그인 파일을 변경한 커밋을 만들기 전에 확인:

- [ ] plugin.json의 version을 올렸는가?
- [ ] marketplace.json의 해당 플러그인 version을 동일하게 올렸는가?
- [ ] 두 version 값이 일치하는가?
