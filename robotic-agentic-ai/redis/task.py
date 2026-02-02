import json
import uuid

import redis

r = redis.Redis(decode_responses=True)


def send_task(skill: str, params: dict):
    task_id = str(uuid.uuid4())

    r.xadd(
        "robot.tasks",
        {"task_id": task_id, "skill": skill, "params": json.dumps(params)},
    )

    print(f"[LangGraph] Sent task {task_id}")
    return task_id


# send_task("pick", {"object": "cube", "approach": "top"})
