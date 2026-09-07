# Drill 공통 원본

`skills/`, `agents/`, `references/`, `templates/`만 여기서 고친다.

`python3 scripts/sync-drill-platforms.py`를 실행하면 다음 두 플러그인을 생성한다.

- `plugins/drill`: Claude Code용. Claude Agent 메타데이터와 `Task`·`AskUserQuestion` 용어를 유지한다.
- `plugins/drill-codex`: Codex용. 분석 역할을 `references/agents/`로 옮기고 Codex 하위 에이전트 위임 규칙을 넣는다.

플랫폼별 `plugin.json`과 marketplace 파일은 각 플러그인에서 따로 관리한다. 생성 결과를 직접 수정하지 않는다.
