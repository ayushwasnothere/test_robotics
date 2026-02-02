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

The repository follows a **layered skill architecture**, where all robot capabilities are organized by *type of control* rather than by demo or task.

```
agentic-robotics/
├── robot-skill-library/
│   ├── common_action_library/
│   │   ├── core_motion/          # Motion planning (MoveIt 2)
│   │   ├── end_effector/         # Gripper control
│   │   └── process_actions/      # Pouring, rotating, verification
│   │
│   ├── pick_place/               # Task-level orchestration (no new actions)
│   ├── stacking/                 # Task-level orchestration
│   └── liquid_mixing/             # Task-level orchestration
│
├── robotic-agentic-ai/
│   ├── planner/
│   ├── executor/
│   └── verifier/
│
└── docs/
```

---

### Why This Structure?

This structure reflects the **true architectural separation** of the system:

* `core_motion/` contains *how the robot moves* (MoveIt 2 planning, IK, trajectories)
* `end_effector/` contains *how the robot grasps and releases objects*
* `process_actions/` contains *task semantics* such as pouring, rotating, and verification

Task folders (`pick_place`, `stacking`, `liquid_mixing`) **do not define new low-level actions**. Instead, they:

* compose existing actions from `common_action_library`
* define task-specific pipelines or sequences
* serve as reference implementations for students

This design ensures:

* zero duplication of low-level skills
* maximum reuse across tasks
* seamless integration with agentic planners

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

## 8. Skill-to-Implementation Mapping (Skill → Folder → MoveIt API)

This table clarifies **where each skill lives**, **what type of control it represents**, and **which MoveIt 2 or ROS 2 APIs are typically used** to implement it.

| Skill                           | Folder             | Primary Control Type      | MoveIt 2 / ROS 2 APIs Involved                                   |
| ------------------------------- | ------------------ | ------------------------- | ---------------------------------------------------------------- |
| `go_home()`                     | `core_motion/`     | Motion planning           | `MoveGroupInterface::setJointValueTarget`, `plan()`, `execute()` |
| `move_to_pose(pose)`            | `core_motion/`     | Motion planning           | `setPoseTarget`, `setPlanningPipelineId`, `plan()`               |
| `move_linear(delta_xyz)`        | `core_motion/`     | Cartesian motion          | `computeCartesianPath`, `execute()`                              |
| `approach_pose(pose, z_offset)` | `core_motion/`     | Motion planning           | `setPoseTarget` with offset pose                                 |
| `retract(z)`                    | `core_motion/`     | Motion planning           | `computeCartesianPath`                                           |
| `set_motion_speed(profile)`     | `core_motion/`     | Trajectory scaling        | `setMaxVelocityScalingFactor`, `setMaxAccelerationScalingFactor` |
| `gripper_open()`                | `end_effector/`    | Gripper control           | ROS 2 action/service (`GripperCommand`, GPIO)                    |
| `gripper_close(force)`          | `end_effector/`    | Gripper control           | ROS 2 action/service with force limits                           |
| `verify_grasp()`                | `end_effector/`    | State verification        | Gripper state topic, effort/width feedback                       |
| `grasp_container(id)`           | `process_actions/` | Composite action          | Calls motion + gripper skills                                    |
| `release_container(id)`         | `process_actions/` | Composite action          | Calls gripper + retract                                          |
| `pour_liquid(source, target)`   | `process_actions/` | Process action            | Wrist joint control, timed execution                             |
| `rotate_container(container)`   | `process_actions/` | Process action            | Joint-space rotation (`setJointValueTarget`)                     |
| `verify_color(color)`           | `process_actions/` | Perception / verification | Camera node, OpenCV/vision pipeline                              |

> **Important:** Skills in `process_actions/` are *compositions* of lower-level skills. They do not replace MoveIt; they orchestrate MoveIt-based motion and gripper control.

---

## 9. Worked Example: Create Green Color by Mixing Liquids

This section demonstrates how the architecture executes a **process-oriented manipulation task** using the instruction:

> **"Create green color by mixing liquids"**

---

### 8.1 User Instruction

**Input**

```
Create green color
```

The user specifies *what* outcome is desired, not *how* to perform it.

---

### 8.2 Agentic Planner (LLM-based)

#### Intent Parsing

```json
{
  "task_type": "liquid_mixing",
  "target_color": "green"
}
```

#### Domain Knowledge Reasoning

```
green = blue + yellow
```

#### Feasibility Check

The planner confirms the availability of required skills:
* grasp container
* pour liquid
* rotate container
* verify color

#### Action Sequencing

```json
[
  "grasp_container(blue_tube)",
  "pour_liquid(blue_tube, beaker)",
  "release_container(blue_tube)",

  "grasp_container(yellow_tube)",
  "pour_liquid(yellow_tube, beaker)",
  "release_container(yellow_tube)",

  "grasp_container(beaker)",
  "rotate_container(beaker)",
  "verify_color(green)"
]
```

---

### 8.3 Executor / FSM

The executor:

* executes one action at a time
* applies safety checks before each step
* retries or aborts on failure

The executor does **not** replan or reason.

---

### 8.4 Action Library (ROS 2 + MoveIt 2)

* **Motion planning**: MoveIt 2 (IK, collision-free trajectories)
* **Gripper control**: open/close with force limits
* **Process actions**: controlled pouring and rotation

---

### 8.5 Verification

The `verify_color(green)` skill:

* captures an image of the beaker
* computes average color (HSV/RGB)
* validates against a green threshold

---

### 8.6 Outcome

If verification succeeds:

> **"Green color successfully created by mixing blue and yellow liquids."**

If verification fails, the system explains possible causes.

---

## 9. Safety Model

Safety is enforced **outside the agent**:

* LLM never sends joint commands
* All motion goes through MoveIt
* Workspace limits are enforced
* Execution stops immediately on failure

---

## 10. Extensibility

This architecture scales naturally:

* New skills add new capabilities
* Learned policies can replace skills
* Perception can be integrated later

A learned policy is treated as:

> **Just another skill**

---

## 11. Summary

This project demonstrates a **modern, safe, and scalable approach** to intelligent robotic manipulation by combining:

* ROS 2 + MoveIt 2 for control
* Skill-based manipulation
* Agentic AI for reasoning and planning

The result is a system that can **think, decide, act, and explain** — without compromising safety.

