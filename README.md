# Skills

A fork of [huggingface/skills](https://huggingface.co/skills) — a platform for discovering, evaluating, and sharing AI skills/tools as plugins for coding assistants like Claude and Cursor.

## Overview

Skills are modular AI capabilities that can be integrated into your development workflow. This repository contains:

- **Plugin manifests** for Claude and Cursor integrations
- **Automated workflows** for generating agents and pushing leaderboards
- **Marketplace listings** for skill discovery

## Plugin Integrations

### Claude Plugin
The Claude plugin manifest is located at `.claude-plugin/plugin.json`. It defines the skill's capabilities, endpoints, and marketplace metadata.

### Cursor Plugin
The Cursor plugin manifest is located at `.cursor-plugin/plugin.json`. It provides similar integration for the Cursor IDE.

## Marketplace

Browse available skills in the marketplace:
- `.claude-plugin/marketplace.json` — Skills available for Claude
- `.cursor-plugin/marketplace.json` — Skills available for Cursor

## Leaderboards

This project maintains two leaderboards:

- **Evals Leaderboard** — Tracks skill performance on standardized evaluations
- **Hackers Leaderboard** — Tracks contributor activity and skill submissions

Leaderboards are automatically updated via GitHub Actions workflows.

## GitHub Actions Workflows

| Workflow | Description |
|---|---|
| `generate-agents.yml` | Automatically generates agent configurations from skill definitions |
| `push-evals-leaderboard.yml` | Pushes updated evals leaderboard to HuggingFace Hub |
| `push-hackers-leaderboard.yml` | Pushes updated hackers leaderboard to HuggingFace Hub |

## Security

Please review our [Security Policy](.github/workflows/SECURITY.md) before reporting vulnerabilities.

## Contributing

1. Fork this repository
2. Add or modify a skill definition
3. Submit a pull request
4. Your skill will be evaluated and added to the leaderboard

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.
