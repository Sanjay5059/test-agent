from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.weather_tool import get_weather
from tools.fitness_tool import create_jogging_plan

SYSTEM_PROMPT = """
You are an autonomous fitness planning agent.

Workflow:
1. Check weather.
2. Analyze conditions carefully.
3. Create jogging strategy.
4. Give practical recommendations.
5. Explain reasoning briefly.
"""


def run_planner_agent(query: str, model: str) -> str:
    llm = ChatOpenAI(model=model)
    agent = create_agent(
        model=llm,
        tools=[get_weather, create_jogging_plan],
        system_prompt=SYSTEM_PROMPT
    )

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    return response["messages"][-1].content
