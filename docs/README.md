# Architecture Overview

## Agentic Robotics: Skill-Based Manipulation and Task Planning

---

## 1. System Philosophy

This project follows a **skill-based, agentic robotics architecture**, where:

* **Low-level robot control** is deterministic and implemented using **ROS 2 + MoveIt 2**
* **High-level reasoning and planning** is performed by an **agentic AI**
* The agent **never controls hardware directly**
* All robot interaction happens via a **shared action (skill) library**

This separation ensures **safety, modularity, reuse, and scalability**.

---

## 2. High-Level Architecture

```
+----------------------+
|   User Instruction   |
|  (Text / Interface)  |
+----------+-----------+
           |
           v
+----------------------+
|  Agentic Planner     |
|  (LLM-based)         |
|  - Intent parsing    |
|  - Feasibility check |
|  - Action sequencing |
+----------+-----------+
           |
           v
+----------------------+
|  Executor / FSM      |
|  (Deterministic)     |
|  - Step execution    |
|  - Retry / abort     |
|  - Safety gating     |
+----------+-----------+
           |
           v
+----------------------+
| Action Library       |
| (ROS 2 + MoveIt 2)   |
| - Motion planning    |
| - Gripper control    |
| - Process actions    |
+----------+-----------+
           |
           v
+----------------------+
|   Robot Hardware     |
|  (Arm, Gripper, IO)  |
+----------------------+
```

---

## 3. Core Design Principles

### 3.1 Separation of Concerns

| Layer          | Responsibility                       |
| -------------- | ------------------------------------ |
| Agentic AI     | What to do and in what order         |
| Executor       | How and when to execute              |
| Action Library | How actions are physically performed |
| Robot          | Physical execution                   |

This separation ensures that:

* LLM errors cannot directly damage hardware
* Robotics code remains testable and deterministic
* AI logic can evolve independently

---

### 3.2 Skill-Based Control

The robot exposes its capabilities as **skills (actions)** such as:

* `pick_object`
* `place_object`
* `compute_stack_pose`
* `pour_liquid`

Each skill:

* has clear inputs and outputs
* performs safety checks
* either succeeds or fails explicitly

The agent plans **over skills**, not over joints or trajectories.

---

## 4. Repository Structure and Responsibilities

```
agentic-robotics/
├── robot-skill-library/
│   ├── common_action_library/
│   ├── pick_place/
│   ├── stacking/
│   └── liquid_mixing/
│
├── robotic-agentic-ai/
│   ├── planner/
│   ├── executor/
│   └── verifier/
│
└── docs/
```

---

## 5. Robot Skill Library

### 5.1 `common_action_library/`

This is the **shared, reusable action library**.

It contains:

* core motion actions
* end-effector actions
* manipulation primitives
* safety utilities

All teams **must contribute reusable actions here**.

> If an action can be reused by another task, it belongs in `common_action_library`.

---

### 5.2 Task-Specific Folders

| Folder           | Purpose                         |
| ---------------- | ------------------------------- |
| `pick_place/`    | Pick & place task orchestration |
| `stacking/`      | Cube stacking logic             |
| `liquid_mixing/` | Liquid pouring and mixing       |

These folders:

* **must not duplicate** common actions
* only contain **task-level pipelines**
* demonstrate how to compose skills

---

## 6. Robotic Agentic AI Module

```
robotic-agentic-ai/
├── planner/
├── executor/
└── verifier/
```

---

### 6.1 Planner

Responsibilities:

* Interpret user instructions
* Convert language → structured goals
* Check feasibility against available skills
* Produce an ordered action plan

Example output:

```json
[
  "pick_object(blue_cube)",
  "place_object(red_box)"
]
```

---

### 6.2 Executor

Responsibilities:

* Execute one action at a time
* Enforce execution order
* Stop on failure
* Handle retries and aborts
* Maintain execution state

The executor is typically implemented as:

* a **finite state machine**
* or a **LangGraph execution graph**

---

### 6.3 Verifier

Responsibilities:

* Verify task success
* Validate physical outcomes
* Confirm final goal conditions

Examples:

* verify object is inside a box
* verify cube stacking stability
* verify resulting liquid color

---

## 7. Agentic Workflow (End-to-End)

1. User provides a high-level instruction
2. Planner parses intent and goals
3. Planner checks if task is feasible
4. Planner generates an action sequence
5. Executor executes actions step-by-step
6. Verifier checks success
7. System reports success or explains failure

---

## 8. Safety Model

Safety is enforced **outside the agent**.

### Key rules:

* LLM never sends joint commands
* All motion goes through MoveIt
* Workspace limits are enforced
* Execution stops immediately on failure

This makes the system **safe-by-design**.

---

## 9. Extensibility

This architecture is designed to scale:

* Add new skills → agent gains new abilities
* Replace hand-coded skills with learned policies
* Integrate perception or vision later
* Swap planning frameworks without touching robotics code

A learned policy (e.g., LeRobot) is treated as:

> **Just another skill**

---

## 10. Educational Value

Students learn:

* real-world robotics software architecture
* abstraction and modular design
* safe use of AI in physical systems
* how industry-grade robot stacks are built

---

## 11. Summary

This project demonstrates a **modern, safe, and scalable approach** to building intelligent robotic systems by combining:

* ROS 2 + MoveIt 2 for control
* Skill-based manipulation
* Agentic AI for reasoning and planning

The result is a system that can **think, decide, act, and explain** — without compromising safety.

