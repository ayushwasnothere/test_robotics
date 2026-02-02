from typing import List

import yaml

from executor.state import SkillCall


def check_skills_validity(unchecked_skills: List[SkillCall]) -> List[SkillCall]:
    with open("planner/skills.yaml") as f:
        skill_catalog = yaml.safe_load(f)

    skills_by_name = {skill["name"]: skill["args"] for skill in skill_catalog["skills"]}

    for step_idx, skill_call in enumerate(unchecked_skills):
        name = skill_call["skill_name"]
        args = skill_call["arguments"]

        if name not in skills_by_name:
            raise ValueError(f"[Step {step_idx}] Unknown skill: '{name}'")

        expected_args = skills_by_name[name]

        if len(args) != len(expected_args):
            raise ValueError(
                f"[Step {step_idx}] Skill '{name}' expects "
                f"{len(expected_args)} arguments {expected_args}, "
                f"but got {list(args.keys())}"
            )

        for param in expected_args:
            if param not in args:
                raise ValueError(
                    f"[Step {step_idx}] Missing argument '{param}' "
                    f"for skill '{name}'"
                )

        for arg in args:
            if arg not in expected_args:
                raise ValueError(
                    f"[Step {step_idx}] Unexpected argument '{arg}' "
                    f"for skill '{name}'"
                )

    return unchecked_skills
