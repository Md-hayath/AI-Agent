"""
Orchestrator Agent - Reads task manifest and delegates to specialized agents.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

from agents.click_install_agent import ClickInstallAgent
from agents.cli_setup_agent import CLISetupAgent
from agents.file_copy_agent import FileCopyAgent
from agents.system_config_agent import SystemConfigAgent
from utils.logger import setup_logger

logger = setup_logger("orchestrator")


class OrchestratorAgent:
    """
    Reads tasks/manifest.json and routes each task to the correct agent.

    Task types:
      - click_install   → ClickInstallAgent   (GUI / package-manager installs)
      - cli_setup       → CLISetupAgent       (terminal-based setup)
      - file_copy       → FileCopyAgent       (copy files to destination)
      - system_config   → SystemConfigAgent   (env vars, hosts, sysctl, etc.)
    """

    AGENT_MAP = {
        "click_install": ClickInstallAgent,
        "cli_setup":     CLISetupAgent,
        "file_copy":     FileCopyAgent,
        "system_config": SystemConfigAgent,
    }

    def __init__(self, manifest_path: str = "tasks/manifest.json"):
        self.manifest_path = Path(manifest_path)

    # ------------------------------------------------------------------
    def _load_manifest(self) -> List[Dict[str, Any]]:
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {self.manifest_path}")
        with open(self.manifest_path) as f:
            data = json.load(f)
        return data.get("tasks", [])

    # ------------------------------------------------------------------
    async def run_all_tasks(self) -> List[Dict[str, Any]]:
        tasks = self._load_manifest()
        results = []

        print(f"  Found {len(tasks)} task(s) to execute.\n")
        print("─" * 60)

        for idx, task in enumerate(tasks, 1):
            task_type = task.get("type")
            task_name = task.get("name", f"Task #{idx}")
            enabled   = task.get("enabled", True)

            print(f"\n[{idx}/{len(tasks)}] {task_name}")
            print(f"      Type    : {task_type}")

            if not enabled:
                print("      Status  : SKIPPED (disabled in manifest)")
                results.append({"name": task_name, "status": "skipped", "message": "disabled"})
                continue

            AgentClass = self.AGENT_MAP.get(task_type)
            if not AgentClass:
                msg = f"Unknown task type '{task_type}'"
                logger.error(msg)
                results.append({"name": task_name, "status": "error", "message": msg})
                continue

            agent = AgentClass(task)
            result = await agent.execute()
            result["name"] = task_name
            results.append(result)

            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"      Status  : {status_icon}  {result['status'].upper()}")
            if result.get("message"):
                print(f"      Message : {result['message']}")

        print("\n" + "─" * 60)
        return results