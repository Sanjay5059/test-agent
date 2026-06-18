from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.weather_tool import get_weather
from tools.fitness_tool import jogging_advice

SYSTEM_PROMPT = """
You are a fitness and weather assistant.

Workflow:
1. First check weather.
2. Then analyze weather.
3. Then provide jogging advice.
4. Keep answers short and practical.
"""


def run_reasoning_agent(query: str, model: str) -> str:
    llm = ChatOpenAI(model=model)
    agent = create_agent(
        model=llm,
        tools=[get_weather, jogging_advice],
        system_prompt=SYSTEM_PROMPT
    )

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    return response["messages"][-1].content
