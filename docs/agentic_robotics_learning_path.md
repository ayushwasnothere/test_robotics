# Agentic Robotics Learning Path

This document provides a **curated, structured learning path** for Computer Science students transitioning from core ML concepts to agentic robotics systems. **Please follow this sequence strictly** to avoid fragmented or shallow understanding.

---

## 1. Big Picture Progression

```
ML → DL → Attention → LLM Behavior
→ Planning & Failure Modes
→ LangChain (Tools & Structure)
→ LangGraph (Execution & Safety)
→ Agentic Robotics Project
```

Each stage builds a *new abstraction* on top of the previous one. Skipping stages will cause confusion later in the project.

---

## 2. Structured Resource Map (What to Study Where)

```
ML           → Google ML Crash Course
DL           → 3Blue1Brown + Goodfellow (Intro)
Attention    → Illustrated Transformer
Transformers → Attention Is All You Need
LLMs         → Stanford CS25
```

Stick to the listed resources only. Do **not** randomly search the internet at this stage.

---

## 3. Machine Learning (ML)

**Goal:** Understand ML as *learning a function from data using loss minimization*.

### Required Topics
- What is Machine Learning?
- Loss
- Training and Test Sets

### Resource
- Google ML Crash Course  
  https://developers.google.com/machine-learning/crash-course

---

## 4. Deep Learning (DL) — Representation Learning

**Goal:** Understand why neural networks learn features automatically instead of humans designing them.

### Required Reading (Selective)

- **Chapter 1: Introduction**  
  https://www.deeplearningbook.org/contents/intro.html

- **Chapter 6: Deep Feedforward Networks**  
  *(Conceptual understanding only — ignore mathematical proofs)*  
  https://www.deeplearningbook.org/contents/mlp.html

### Visual Intuition (Mandatory)

- Neural Networks — 3Blue1Brown  
  *Videos 1–4 only*  
  https://youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi

---

## 5. Attention — Selective Computation

**Goal:** Understand why models must focus on *relevant information* instead of processing everything equally.

### Resource
- Illustrated Transformer  
  https://jalammar.github.io/illustrated-transformer/

Read this **before** touching any Transformer paper.

---

## 6. Transformers & LLM Behavior

**Goal:** Understand Transformers as scalable reasoning architectures and LLMs as probabilistic reasoning systems.

### Transformers (Architecture Focus)
- *Attention Is All You Need* (Read for ideas, not equations)

### LLM Systems Perspective
- Stanford CS25 — Transformers & Large Language Models  
  https://web.stanford.edu/class/cs25/

Focus on:
- Model behavior
- Scaling
- Failure modes
- Limitations

---

## 7. Planning & Failure Modes (Critical Transition)

Before using any agent framework, you must understand:
- Why LLM outputs are unreliable
- Why plans must be verified
- Why execution must be deterministic
- Why failures must be handled outside the model

This understanding is **mandatory** before proceeding further.

---

## 8. LangChain — Tools & Structure

**Goal:** Use LLMs in a controlled, structured manner.

### Topics to Study
- Tools
- Structured Output
- Function Calling

⚠️ Ignore conversational agents, memory systems, and vector databases for now.

---

## 9. LangGraph — Execution & Safety

**Goal:** Build deterministic, safe execution flows around LLM reasoning.

### Topics to Study
- What is a graph?
- State
- Conditional edges

LangGraph will be used to implement:
- Executors
- Retry logic
- Abort conditions
- Safety gating

---

## 10. Agentic Robotics Project

After completing all the above stages, you will be ready to:
- Design agentic planners
- Build deterministic executors
- Integrate skill libraries
- Verify outcomes
- Safely apply AI to physical robotic systems

---

## Final Instruction to Students

> **Do not jump ahead.**  
> **Do not skip conceptual stages.**  
> **Frameworks are tools — understanding is mandatory.**

Follow this path carefully. It is designed to make you a strong Computer Science engineer *before* you become an agentic robotics developer.
