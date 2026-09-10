# flex-hyuntae Claude Plugins

flex 프로젝트와 위키 작업을 위한 `flex-workflow` 마켓이다.

```sh
claude plugin marketplace add flex-hyuntae/claude-plugins
claude plugin install flex-workflow@flex-hyuntae-plugins
```

[flex-workflow 사용법](plugins/flex-workflow/README.md)을 참고한다.

## Drill·Rules 이전

Drill과 Rules는 [eomttt/agent-plugins](https://github.com/eomttt/agent-plugins)로 옮겼다.
이 레포에서는 두 플러그인을 더 이상 배포하지 않는다.
새 마켓 `eomttt-plugins`에는 다음 패키지가 있다.

| 기능 | Claude Code | Codex |
| --- | --- | --- |
| Drill | `drill-claude` | `drill-codex` |
| Rules | `rules-claude` | `rules-codex` |

새 패키지를 설치한 뒤 기존 `drill@flex-hyuntae-plugins`, `rules@flex-hyuntae-plugins`를 제거한다.
비공개 새 레포의 접근 권한과 설치 방법은 새 레포에서 확인한다.

## 수정

`plugins/flex-workflow/`에서 수정하고 [AGENTS.md](AGENTS.md)의 버전·검증 절차를 따른다.
