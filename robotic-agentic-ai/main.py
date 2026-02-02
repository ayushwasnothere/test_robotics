import json
from typing import cast

from executor.graph import build_executor
from executor.state import ExecState
from planner.planner import plan
from verifier.skill_validator import check_skills_validity


def load_world_state():
    with open("planner/world_state.json") as f:
        return json.load(f)


def main():

    world_state = load_world_state()
    action_plan = plan("Create green color", world_state)
    action_plan = check_skills_validity(action_plan)

    initial_state = cast(
        ExecState,
        {
            "plan": action_plan,
            "step": 0,
            "retries": 0,
            "last_ok": None,
            "outcome": None,
        },
    )
    executor = build_executor()

    executor.invoke(initial_state)


if __name__ == "__main__":
    main()
