# flex-hyuntae claude plugins

Personal Claude Code plugin marketplace.

## Usage

### Add marketplace

```shell
/plugin marketplace add flex-hyuntae/claude-plugins
```

### Install a plugin

```shell
/plugin install git@flex-hyuntae-plugins
/plugin install drill@flex-hyuntae-plugins
/plugin install code-review@flex-hyuntae-plugins
/plugin install flex-workflow@flex-hyuntae-plugins
/plugin install rules@flex-hyuntae-plugins
```

### Update marketplace

```shell
/plugin marketplace update
```

## Plugins

| Plugin | Description | Commands | Agents |
|--------|-------------|----------|--------|
| [git](plugins/git/README.md) | Git workflow automation | `commit`, `create-pr`, `rebase-stack` | — |
| [drill](plugins/drill/README.md) | Spec/Concept 기반 개발 워크플로우 | `drill`, `plan`, `prepare`, `review`, `qa` | — |
| [code-review](plugins/code-review/README.md) | Comprehensive code review | — | `code-review` |
| [flex-workflow](plugins/flex-workflow/README.md) | flex project workflows | `deploy`, `test-package`, `add-til`, `daily-summary` | `i18n-convert` |
| [rules](plugins/rules/README.md) | 코딩 컨벤션과 성능 최적화 규칙 (35개) | `add` | — |

## Adding a Plugin

1. Create `plugins/<plugin-name>/` directory
2. Add `.claude-plugin/plugin.json` manifest
3. Add files in `skills/` and/or `agents/`
4. Add entry to `.claude-plugin/marketplace.json` `plugins` array
5. Bump `version` in both `plugin.json` and `marketplace.json`
6. Validate with `claude plugin validate .` or `/plugin validate .`
7. Commit and push