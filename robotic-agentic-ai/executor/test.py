import json
import random
import time

import redis

r = redis.Redis(decode_responses=True)

TASK_STREAM = "robot.tasks"
EVENT_STREAM = "robot.events"

TASK_GROUP = "ros_bridge"
CONSUMER = "dummy_bridge_1"

EXECUTION_TIME_SEC = 2
FAIL_PROBABILITY = 0.3  # 30% failure rate


def execute_fake_skill(task):
    """
    Simulate robot execution.
    """
    skill = task["skill"]
    params = json.loads(task["params"])

    print(f"[DUMMY BRIDGE] Executing skill={skill}, params={params}")

    time.sleep(EXECUTION_TIME_SEC)

    # Deterministic failure hook (optional)
    if skill == "fail":
        return False, "FORCED_FAILURE"

    # Random failure
    if random.random() < FAIL_PROBABILITY:
        return False, "SIMULATED_FAILURE"

    return True, None


print("[DUMMY BRIDGE] Started")

while True:
    messages = r.xreadgroup(
        TASK_GROUP, CONSUMER, {TASK_STREAM: ">"}, count=1, block=5000
    )

    for _, entries in messages:
        for msg_id, task in entries:
            task_id = task["task_id"]

            success, reason = execute_fake_skill(task)

            # ACK task
            r.xack(TASK_STREAM, TASK_GROUP, msg_id)

            # Emit result event
            r.xadd(
                EVENT_STREAM,
                {
                    "task_id": task_id,
                    "status": "SUCCESS" if success else "FAILED",
                    "reason": reason or "",
                },
            )

            print(
                f"[DUMMY BRIDGE] Task {task_id} -> "
                f"{'SUCCESS' if success else 'FAILED'}"
            )
