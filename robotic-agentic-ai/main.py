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
    tests=["pick and place the tube_1 from ground and place it on a table "]
    action_plan = plan(tests[0], world_state)
    print(json.dumps(action_plan, indent=2))
    action_plan = check_skills_validity(action_plan)
    print("\n\n\nValidated Action Plan:")
    print(json.dumps(action_plan, indent=2))
    
    initial_state = cast(
        ExecState,
        {
            "plan": action_plan,
            "step": 0,
            "retries": 0,
            "last_ok": None,
            "outcome": None,
            "current_task_id": None,
        },
    )
    executor = build_executor()

    executor.invoke(initial_state)


if __name__ == "__main__":
    main()
