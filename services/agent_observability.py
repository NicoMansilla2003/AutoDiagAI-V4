"""CrewAI callbacks for recording bounded agent execution."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def iteration_limit_callback(agent_name: str, max_iter: int):
    steps = 0

    def record_step(_step) -> None:
        nonlocal steps
        steps += 1
        if steps == max_iter:
            logger.warning(
                "agent_iteration_ceiling_reached",
                extra={"agent": agent_name, "max_iter": max_iter},
            )

    return record_step
