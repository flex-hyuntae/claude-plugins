# Claude·Codex 프로젝트 지침

## 플러그인 버전 관리 규칙

`plugins/<name>/` 하위 파일을 수정·추가·삭제할 때 (README.md 제외) **반드시** 버전을 올린다.

### 업데이트 대상 (두 곳 동시)

1. `plugins/<name>/.claude-plugin/plugin.json` → `version`
2. `.claude-plugin/marketplace.json` → 해당 플러그인의 `version`

두 값은 항상 동일해야 한다.

### 버전 결정 로직

형식: `YYYY.MM.DD.N` — 오늘 날짜 기준으로 판단한다. **세그먼트는 항상 4개**이고, 날짜가 바뀌어도 `.N` 을 생략하지 않는다 (`2026.07.30` 같은 3세그먼트 버전은 쓰지 않는다).

| 기존 버전의 날짜 | 새 버전 |
|------------------|---------|
| 오늘이 아님 | 오늘 날짜 + `.1` |
| 오늘과 같음 | 날짜 유지, `N` 을 +1 |

예 — 오늘이 `2026-07-30` 일 때:

| 기존 | 새 버전 |
|------|---------|
| `2026.07.27.1` | `2026.07.30.1` |
| `2026.07.30.1` | `2026.07.30.2` |

### 커밋 전 체크리스트

플러그인 파일을 변경한 커밋을 만들기 전에 확인:

- [ ] plugin.json의 version을 올렸는가?
- [ ] marketplace.json의 해당 플러그인 version을 동일하게 올렸는가?
- [ ] 두 version 값이 일치하는가?

## Drill 소스 분리

`rules`와 `flex-workflow`는 이 레포의 `plugins/`에서 관리한다.
Drill의 새 소스는 `~/Projects/eomttt/agent-plugins/shared/drill`이다. 해당 레포의 `AGENTS.md`를 따른다.
이 레포에 남아 있는 Drill 사본은 새 변경의 원본으로 쓰지 않는다.
공통 지침은 `AGENTS.md`에 작성하고 `CLAUDE.md`는 이 파일의 참조만 유지한다.
