"""Orchestrator agent for setup tasks."""

from pathlib import Path
from typing import List

from agents.llm_agent import LLMAgent
from tasks.handlers import TaskHandler
from tasks.models import TaskResult
from tasks.parser import load_manifest
from utils.logger import setup_logger

logger = setup_logger("orchestrator")


class OrchestratorAgent:
    """Loads task definitions and executes them in order."""

    def __init__(self, manifest_path: Path, dry_run: bool = True) -> None:
        self.manifest_path = manifest_path
        self.dry_run = dry_run
        self.handler = TaskHandler(dry_run=dry_run)
        self.llm = LLMAgent()

    async def run_all_tasks(self) -> List[TaskResult]:
        tasks = load_manifest(self.manifest_path)
        results: List[TaskResult] = []

        logger.info("Loaded %d task(s) from %s", len(tasks), self.manifest_path)
        for task in tasks:
            logger.info("Running task [%s] %s", task.task_type, task.name)
            result = await self.handler.execute(task)
            if not result.success and self.llm.is_configured():
                suggestion = self.llm.suggest_fix(
                    task_name=task.name,
                    task_type=task.task_type,
                    error_output=result.message,
                )
                result.message = f"{result.message}\nLLM suggestion:\n{suggestion}"
            results.append(result)

        return results
