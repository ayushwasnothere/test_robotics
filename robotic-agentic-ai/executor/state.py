from typing import List, Optional, TypedDict


class SkillCall(TypedDict):
    skill_name: str
    arguments: dict[str, str]


class ExecState(TypedDict):
    plan: List[dict]
    step: int
    retries: int
    last_ok: bool
    current_task_id: Optional[str]
    outcome: Optional[str]
