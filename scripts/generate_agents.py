#!/usr/bin/env python3
"""
Generate agent definitions from skills marketplace configuration.

This script reads the marketplace.json files and generates agent YAML/JSON
definitions that can be deployed to supported platforms.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).parent.parent
CLAUDE_MARKETPLACE = ROOT_DIR / ".claude-plugin" / "marketplace.json"
CURSOR_MARKETPLACE = ROOT_DIR / ".cursor-plugin" / "marketplace.json"
OUTPUT_DIR = ROOT_DIR / "agents"


def load_json(path: Path) -> dict[str, Any]:
    """Load and parse a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict[str, Any], path: Path) -> None:
    """Save data as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def generate_claude_agents(marketplace: dict[str, Any]) -> list[dict[str, Any]]:
    """Transform Claude plugin marketplace entries into agent definitions."""
    agents = []
    skills = marketplace.get("skills", [])

    for skill in skills:
        agent = {
            "id": skill.get("id", ""),
            "name": skill.get("name", ""),
            "description": skill.get("description", ""),
            "platform": "claude",
            "version": skill.get("version", "0.1.0"),
            "capabilities": skill.get("capabilities", []),
            "parameters": skill.get("parameters", {}),
            "tags": skill.get("tags", []),
        }
        agents.append(agent)

    return agents


def generate_cursor_agents(marketplace: dict[str, Any]) -> list[dict[str, Any]]:
    """Transform Cursor plugin marketplace entries into agent definitions."""
    agents = []
    skills = marketplace.get("skills", [])

    for skill in skills:
        agent = {
            "id": skill.get("id", ""),
            "name": skill.get("name", ""),
            "description": skill.get("description", ""),
            "platform": "cursor",
            "version": skill.get("version", "0.1.0"),
            "triggers": skill.get("triggers", []),
            "actions": skill.get("actions", []),
            "tags": skill.get("tags", []),
        }
        agents.append(agent)

    return agents


def merge_agents(
    claude_agents: list[dict[str, Any]],
    cursor_agents: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge agents from multiple platforms, deduplicating by skill ID."""
    merged: dict[str, dict[str, Any]] = {}

    for agent in claude_agents + cursor_agents:
        skill_id = agent["id"]
        if skill_id not in merged:
            merged[skill_id] = {"id": skill_id, "platforms": []}
        merged[skill_id]["platforms"].append(agent["platform"])
        # Carry over shared metadata from the first occurrence
        for key in ("name", "description", "version", "tags"):
            if key not in merged[skill_id] and key in agent:
                merged[skill_id][key] = agent[key]

    return list(merged.values())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate agent definitions from marketplace configs")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR, help="Directory to write generated agents")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args(argv)

    print(f"Loading Claude marketplace from {CLAUDE_MARKETPLACE}")
    claude_marketplace = load_json(CLAUDE_MARKETPLACE)
    claude_agents = generate_claude_agents(claude_marketplace)
    print(f"  Found {len(claude_agents)} Claude skill(s)")

    print(f"Loading Cursor marketplace from {CURSOR_MARKETPLACE}")
    cursor_marketplace = load_json(CURSOR_MARKETPLACE)
    cursor_agents = generate_cursor_agents(cursor_marketplace)
    print(f"  Found {len(cursor_agents)} Cursor skill(s)")

    all_agents = merge_agents(claude_agents, cursor_agents)
    output = {"agents": all_agents, "total": len(all_agents)}

    output_path = args.output_dir / "agents.json"
    if args.dry_run:
        print("\n[dry-run] Would write to:", output_path)
        print(json.dumps(output, indent=2))
    else:
        save_json(output, output_path)
        print(f"\nWrote {len(all_agents)} agent(s) to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
