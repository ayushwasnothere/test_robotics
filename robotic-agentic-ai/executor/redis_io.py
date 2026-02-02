import json
import time
import uuid

import redis

r = redis.Redis(decode_responses=True)

TASK_STREAM = "robot.tasks"
EVENT_STREAM = "robot.events"
EVENT_GROUP = "langgraph"
EVENT_CONSUMER = "lg_1"


def send_skill(skill: dict) -> str:
    task_id = str(uuid.uuid4())

    r.xadd(
        TASK_STREAM,
        {
            "task_id": task_id,
            "skill": skill["name"],
            "params": json.dumps(skill.get("params", {})),
        },
    )

    print(f"[REDIS] Sent task {task_id}")
    return task_id


def wait_for_result(task_id: str, timeout: int = 30) -> bool:
    start = time.time()

    while time.time() - start < timeout:
        messages = r.xreadgroup(
            EVENT_GROUP,
            EVENT_CONSUMER,
            {EVENT_STREAM: ">"},
            block=5000,
            count=1,
        )

        for _, entries in messages:
            for msg_id, event in entries:
                r.xack(EVENT_STREAM, EVENT_GROUP, msg_id)

                if event.get("task_id") == task_id:
                    status = event.get("status")
                    print(f"[REDIS] Task {task_id} finished: {status}")
                    return status == "SUCCESS"

    print(f"[REDIS] Task {task_id} timed out")
    return False
