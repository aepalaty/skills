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

> **Personal note:** I'm using this fork primarily to experiment with custom skill definitions for local development workflows. PRs here are for my own testing — please contribute to the upstream [huggingface/skills](https://huggingface.co/skills) repo instead.
>
> **Local setup tip:** After cloning, run `cp .env.example .env` and fill in your `HF_TOKEN` before triggering any workflows locally with `act`.
>
> **Sync tip:** To pull in upstream changes without losing local tweaks, run:
> ```bash
> git fetch upstream
> git merge upstream/main --no-edit
> ```
>
> **Debugging tip:** If a workflow fails locally with `act`, try passing `--container-architecture linux/amd64` — this fixed a platform mismatch issue for me on Apple Silicon.
>
> **VS Code tip:** Install the [GitHub Actions extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-github-actions) to get syntax highlighting and validation for the workflow YAML files — makes editing them much less error-prone.
>
> **Workflow caching tip:** I added `cache: pip` to the `setup-python` step in each workflow to speed up repeated local runs with `act`. Cuts install time roughly in half on my machine.
>
> **Token scopes tip:** When creating your `HF_TOKEN`, make sure it has **write** access to your target Space — read-only tokens will cause the leaderboard push workflows to fail silently with a 403.
