#!/usr/bin/env python3
"""Push skills evaluation results to the HuggingFace leaderboard datasets.

This script reads evaluation results from local JSON files and pushes them
to the corresponding HuggingFace Hub datasets for public leaderboard display.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from datasets import Dataset
    from huggingface_hub import HfApi
except ImportError:
    print("Error: Required packages not found. Run: pip install datasets huggingface_hub")
    sys.exit(1)


LEADERBOARD_CONFIGS = {
    "evals": {
        "dataset_id": "huggingface/skills-evals-leaderboard",
        "results_path": "results/evals.json",
        "description": "Skills evaluation leaderboard",
    },
    "hackers": {
        "dataset_id": "huggingface/skills-hackers-leaderboard",
        "results_path": "results/hackers.json",
        "description": "Skills hackers leaderboard",
    },
}


def load_results(results_path: str) -> list[dict]:
    """Load evaluation results from a JSON file.

    Args:
        results_path: Path to the JSON results file.

    Returns:
        List of result records.

    Raises:
        FileNotFoundError: If the results file does not exist.
        ValueError: If the file content is not a valid list.
    """
    path = Path(results_path)
    if not path.exists():
        raise FileNotFoundError(f"Results file not found: {results_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of records in {results_path}, got {type(data).__name__}")

    return data


def enrich_records(records: list[dict]) -> list[dict]:
    """Add metadata fields to each record before pushing.

    Args:
        records: Raw result records.

    Returns:
        Records with added timestamp and schema version.
    """
    # Use a single timestamp for the entire batch so all records in one push are consistent
    timestamp = datetime.utcnow().isoformat()
    enriched = []
    for record in records:
        enriched.append({
            **record,
            "pushed_at": timestamp,
            "schema_version": "1.0",
        })
    return enriched


def push_to_hub(records: list[dict], dataset_id: str, token: str) -> None:
    """Push records to a HuggingFace Hub dataset.

    Args:
        records: List of result records to push.
        dataset_id: Target HuggingFace dataset repository ID.
        token: HuggingFace API token with write access.
    """
    api = HfApi(token=token)

    # Ensure the dataset repo exists, create if needed
    try:
        api.repo_info(repo_id=dataset_id, repo_type="dataset")
    except Exception:
        print(f"Creating dataset repository: {dataset_id}")
        # Create as private by default to avoid accidentally exposing data before it's ready
        api.create_repo(repo_id=dataset_id, repo_type="dataset", private=True)

    dataset = Dataset.from_list(records)
    dataset.push_to_hub(dataset_id, token=token, commit_message="Update leaderboard results")
    print(f"Successfully pushed {len(records)} records to {dataset_id}")
