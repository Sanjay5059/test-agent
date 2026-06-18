from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.weather_tool import get_weather
from tools.calculator_tool import calculator


def run_multi_tool_agent(query: str, model: str) -> str:
    llm = ChatOpenAI(model=model)
    agent = create_agent(model=llm, tools=[get_weather, calculator])

    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    return response["messages"][-1].content
