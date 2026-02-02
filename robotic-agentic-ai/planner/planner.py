import json

import yaml
# from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI

from executor.state import SkillCall
from planner.prompt import PLANNER_PROMPT

# load_dotenv()


def load_skills():
    with open("planner/skills.yaml") as f:
        return yaml.safe_load(f)


def plan(task: str, world_state: dict) -> list[SkillCall]:
    skills = load_skills()

    model = ChatOllama(
        model="gpt-oss:20b",
        base_url="http://10.11.51.217:11434",
        temperature=0,
        reasoning=True,
        reasoning_effort="high",
    )

    # model = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash",
    #     temperature=1.0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    # )

    # model = ChatGroq(
    #     model="openai/gpt-oss-20b",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     reasoning_effort="medium",
    # )

    # model = ChatOpenAI(
    #     model="gpt-5-nano-2025-08-07",
    #     stream_usage=True,
    #     temperature=None,
    #     # max_tokens=None,
    #     timeout=None,
    #     reasoning={"effort": "medium", "summary": "detailed"},
    #     max_retries=2,
    #     # api_key="...",  # If you prefer to pass api key in directly
    #     # base_url="...",
    #     # organization="...",
    #     # other params...
    # )

    formatted_prompt = PLANNER_PROMPT.format(
        skills=json.dumps(skills, indent=0),
        task=task,
        world_state=json.dumps(world_state, indent=0),
    )

    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content=f"Please generate the plan for the task: {task}"),
    ]

    res = model.invoke(messages)
    print(res + "\n\n\n\n")
    response_text = str(res.content).strip()

    return json.loads(response_text)
