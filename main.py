#!/usr/bin/env python3
"""
AI Setup Agent
Runs installation and setup tasks from a manifest.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from agents.orchestrator import OrchestratorAgent
from utils.display import print_banner, print_summary
from utils.env_loader import load_dotenv
from utils.logger import setup_logger

logger = setup_logger("main")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run AI agent setup tasks from JSON manifest."
    )
    parser.add_argument(
        "--manifest",
        default="config/software_manifest.json",
        help="Path to JSON task manifest file.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute commands (default is dry-run).",
    )
    return parser.parse_args()


async def run() -> int:
    load_dotenv()
    args = parse_args()
    manifest_path = Path(args.manifest)

    if not manifest_path.exists():
        logger.error("Manifest file not found: %s", manifest_path)
        return 2

    print_banner()
    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"\nMode: {mode}")
    print(f"Manifest: {manifest_path}\n")

    orchestrator = OrchestratorAgent(
        manifest_path=manifest_path,
        dry_run=not args.execute,
    )
    results = await orchestrator.run_all_tasks()
    print_summary(results)
    return 0 if all(result.success for result in results) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(run()))
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        raise SystemExit(130)