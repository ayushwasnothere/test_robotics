import random

from executor.state import SkillCall


def execute(skill_call: SkillCall) -> bool:
    # random 30% successimulation
    print(f"[SKILL] {skill_call}")

    return random.random() < 0.7
