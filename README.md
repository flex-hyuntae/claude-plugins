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
/plugin install plan@flex-hyuntae-plugins
/plugin install code-review@flex-hyuntae-plugins
/plugin install flex-workflow@flex-hyuntae-plugins
```

### Update marketplace

```shell
/plugin marketplace update
```

## Plugins

| Plugin | Description | Commands |
|--------|-------------|----------|
| [git](plugins/git/README.md) | Git workflow automation | `git-commit`, `github-pr`, `git-rebase-stack` |
| [plan](plugins/plan/README.md) | Project planning support | `deep-interview` |
| [code-review](plugins/code-review/README.md) | Comprehensive code review | `code-review` |
| [flex-workflow](plugins/flex-workflow/README.md) | Flex project workflows | `deploy`, `test-package`, `i18n-convert` |

## Adding a Plugin

1. Create `plugins/<plugin-name>/` directory
2. Add `.claude-plugin/plugin.json` manifest
3. Add command files in `commands/`
4. Add entry to `.claude-plugin/marketplace.json` `plugins` array
5. Bump `version` in both `plugin.json` and `marketplace.json`
6. Validate with `claude plugin validate .` or `/plugin validate .`
7. Commit and push