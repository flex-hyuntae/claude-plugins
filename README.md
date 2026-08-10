# flex-hyuntae claude plugins

Personal Claude Code plugin marketplace.

## Usage

### Add marketplace

```shell
/plugin marketplace add flex-hyuntae/claude-plugins
```

### Install a plugin

```shell
/plugin install drill@flex-hyuntae-plugins
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
| [drill](plugins/drill/README.md) | Spec/Concept 기반 개발 워크플로우 | `drill`, `plan`, `prepare`, `review`, `qa` | — |
| [flex-workflow](plugins/flex-workflow/README.md) | flex project workflows + 위키 기록 | `deploy`, `test-package`, `setup-dev`, `add-topic`, `add-work`, `digest-wiki` | `i18n-convert` |
| [rules](plugins/rules/README.md) | 코딩 컨벤션과 성능 최적화 규칙 (35개) | `add` | — |

## Adding a Plugin

1. Create `plugins/<plugin-name>/` directory
2. Add `.claude-plugin/plugin.json` manifest
3. Add files in `skills/` and/or `agents/`
4. Add entry to `.claude-plugin/marketplace.json` `plugins` array
5. Bump `version` in both `plugin.json` and `marketplace.json`
6. Validate with `claude plugin validate .` or `/plugin validate .`
7. Commit and push