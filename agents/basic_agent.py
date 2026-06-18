from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.weather_tool import get_weather


def run_basic_agent(city: str, model: str) -> str:
    llm = ChatOpenAI(model=model)
    agent = create_agent(model=llm, tools=[get_weather])

    response = agent.invoke({
        "messages": [{"role": "user", "content": f"What is the weather in {city}?"}]
    })

    return response["messages"][-1].content
