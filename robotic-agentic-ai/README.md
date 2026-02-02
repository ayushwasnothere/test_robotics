# Agentic Task Planning and Execution for Robotic Manipulation

## (Robotic Agentic AI Module)

---

## Title

**Robotic Agentic AI: Task Planning and Orchestration Using a Skill-Based Action Library**

---

## 1. Problem Description

You are provided with a **robot skill library** implemented using **ROS 2 and MoveIt 2**, organized according to a **layered skill architecture**:

```
common_action_library/
├── core_motion/          # Motion planning (MoveIt 2)
├── end_effector/         # Gripper control
└── process_actions/      # Task-semantic skills
```

Your task is **not** to control robot joints, trajectories, or grippers.

Instead, you must design and implement an **agentic AI system** that:

* interprets **high-level user instructions**,
* determines **whether a task is feasible** using available skills,
* **plans a sequence of task-semantic actions**,
* executes those actions **via a deterministic executor**, and
* verifies task completion or explains failure.

This module represents the **reasoning and orchestration layer** of the system.

---

## 2. Important Architectural Rule (Read Carefully)

> **The agent plans ONLY over task-semantic skills in `process_actions/`.**

The agent **must NOT**:

* call functions from `core_motion/`
* call functions from `end_effector/`
* reason about poses, joints, IK, or trajectories

Those details are **internal to the robotics layer**.

---

## 3. Action Library Interface (What the Agent Sees)

The agent is given access to **LangChain Tools** that directly correspond to **skills in `process_actions/`**.

### Available Tools (Examples)

| Tool Name             | Description                               | Parameters                             |
| --------------------- | ----------------------------------------- | -------------------------------------- |
| `go_home()`           | Move robot to safe home pose              | —                                      |
| `pick_object()`       | Pick an object                            | `object_id`                            |
| `place_object()`      | Place object at target                    | `target_id`                            |
| `grasp_container()`   | Grasp a container                         | `container_id`                         |
| `release_container()` | Release held container                    | `container_id`                         |
| `pour_liquid()`       | Pour liquid from one container to another | `source_container`, `target_container` |
| `rotate_container()`  | Rotate container to mix                   | `container_id`                         |
| `verify_color()`      | Verify resulting color                    | `expected_color`                       |
| `verify_stack()`      | Verify cube stacking                      | `top_object`, `bottom_object`          |

Each tool:

* has a **clear semantic meaning**
* takes **explicit parameters**
* encapsulates all motion, timing, and safety internally

---

## 4. Supported Tasks (Ground Truth Capabilities)

The system is known to support the following **task-level capabilities**:

### 4.1 Pick & Place

Example:

> “Pick the blue cube and place it in the red box.”

### 4.2 Stacking

Example:

> “Stack the blue cube on the red cube.”

### 4.3 Liquid Mixing

Example:

> “Create green color.”

All object and container locations are **fixed and known** (via an object registry).

---

## 5. Student Task

Design and implement an **agentic planner + executor** that can handle **all three tasks** using the same workflow.

Your implementation must:

1. Parse natural language instructions
2. Convert them into **structured goals**
3. Check **feasibility** using available tools
4. Generate an **ordered sequence of tool calls**
5. Execute them deterministically
6. Verify success or explain failure

---

## 6. Functional Requirements

### R1. Instruction Interpretation

Convert user input into a structured task representation.

Example:

```
Input: "Create green color"
```

Output:

```json
{
  "task_type": "liquid_mixing",
  "target_color": "green"
}
```

---

### R2. Feasibility Checking

Before execution, the agent must verify:

* required tools exist
* required parameters are available

If not feasible, the system must explain **what capability is missing**.

Example:

> “This task is not feasible because no color-verification skill is available.”

---

### R3. Planning (Action Sequencing)

If feasible, the agent must generate an **ordered plan** using **only process-level tools**.

Example (Create Green Color):

```json
[
  "grasp_container(source_container='blue_tube')",
  "pour_liquid(source_container='blue_tube', target_container='beaker')",
  "release_container(container_id='blue_tube')",

  "grasp_container(source_container='yellow_tube')",
  "pour_liquid(source_container='yellow_tube', target_container='beaker')",
  "release_container(container_id='yellow_tube')",

  "grasp_container(container_id='beaker')",
  "rotate_container(container_id='beaker')",
  "verify_color(expected_color='green')"
]
```

---

### R4. Execution (Deterministic Executor)

The agent **does not execute actions directly**.

Instead:

* the executor runs **one tool at a time**
* stops immediately on failure
* never reorders steps on its own

The executor may be implemented as:

* a finite-state machine
* a LangGraph execution graph

---

### R5. Verification and Failure Handling

After execution:

* verification tools must be called
* success or failure must be reported

On failure, the system must:

* explain **what failed**
* explain **why it failed**
* optionally suggest corrective actions

---

### R6. Explainability

The system must be able to explain:

* why a plan was chosen
* why a task was infeasible
* which step failed during execution

---

## 7. Non-Functional Requirements

* The agent must **never send motion commands**
* Planning logic must be **independent of ROS 2**
* Tool calls must be **parameterized**
* Execution must be **safe and deterministic**

---

## 8. Framework Guidelines

Students may use **one** of the following:

* LangChain (Structured Tools)
* LangGraph (recommended for execution)
* OpenAI Agents SDK

The framework choice must preserve:

* tool boundaries
* separation of planning and execution

---

## 9. Teaching Rule (Very Important)

> **If a value can change between tasks, it must be a tool parameter.**
> **If a value concerns physics or safety, it belongs inside the skill.**

---

## 10. Final Instruction to Students

> You are **not building robot skills**.
> You are **not controlling MoveIt**.
> You are building an **agentic reasoning system** that decides:
>
> **what actions to take, in what order, and why.**

---

### ✔ Alignment Guarantee

This document is **fully aligned** with:

* `architecture.md`
* layered skill design
* `process_actions`-only tool exposure
* safe agentic robotics principles

---

If you want next, I can:

* create a **grading rubric** for the agentic-AI team
* add a **reference implementation skeleton**
* produce a **planner–executor sequence diagram**
* or create a **student checklist** for validation

Just tell me.

