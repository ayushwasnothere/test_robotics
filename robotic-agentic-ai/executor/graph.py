from typing import cast

from langgraph.graph import END, StateGraph

from executor.redis_io import send_skill, wait_for_result
from executor.state import ExecState

MAX_RETRIES = 2


def send_step(state: ExecState) -> ExecState:
    if state["step"] >= len(state["plan"]):
        return {
            **state,
            "last_ok": True,
            "current_task_id": None,
        }

    skill = state["plan"][state["step"]]
    task_id = send_skill(skill)

    return {
        **state,
        "current_task_id": task_id,
    }


def after_send(state: ExecState):
    if state["current_task_id"] is None:
        return "update"
    return "wait"


def wait_step(state: ExecState) -> ExecState:
    task_id = state["current_task_id"]
    assert task_id is not None

    ok = wait_for_result(task_id)

    return {
        **state,
        "last_ok": ok,
        "current_task_id": None,
    }


def update_state(state: ExecState) -> ExecState:
    if state["last_ok"]:
        return {
            **state,
            "step": state["step"] + 1,
            "retries": 0,
        }
    return {
        **state,
        "retries": state["retries"] + 1,
    }


def route(state: ExecState):
    if state["last_ok"]:
        if state["step"] >= len(state["plan"]):
            return "success"
        return "send"

    if state["retries"] >= MAX_RETRIES:
        return "abort"

    return "send"


def success_node(state: ExecState) -> ExecState:
    s = dict(state)
    s["outcome"] = "SUCCESS"
    print("[EXECUTOR] Execution completed successfully.")
    return cast(ExecState, s)


def abort_node(state: ExecState) -> ExecState:
    s = dict(state)
    s["outcome"] = "FAILED"
    print("[EXECUTOR] Aborting execution due to repeated failures.")
    return cast(ExecState, s)


def build_executor():
    g = StateGraph(ExecState)

    g.add_node("send", send_step)

    g.add_node("wait", wait_step)
    g.add_node("update", update_state)
    g.add_node("success", success_node)
    g.add_node("abort", abort_node)

    g.set_entry_point("send")

    g.add_conditional_edges(
        "send",
        after_send,
        {
            "wait": "wait",
            "update": "update",
        },
    )
    g.add_edge("wait", "update")

    g.add_conditional_edges(
        "update",
        route,
        {
            "send": "send",
            "success": "success",
            "abort": "abort",
        },
    )

    g.add_edge("success", END)
    g.add_edge("abort", END)

    return g.compile()
