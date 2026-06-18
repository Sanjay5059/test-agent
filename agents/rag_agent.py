from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.weather_tool import get_weather
from tools.rag_tool import search_documents

SYSTEM_PROMPT = """
You are a strict RAG assistant.

Rules:
1. Use ONLY provided tool information.
2. Do not add outside knowledge.
3. Do not hallucinate.
4. Keep answers concise.
"""


def run_rag_agent(chat_history: list, user_input: str, model: str) -> tuple[str, list]:
    llm = ChatOpenAI(model=model)
    agent = create_agent(
        model=llm,
        tools=[get_weather, search_documents],
        system_prompt=SYSTEM_PROMPT
    )

    chat_history.append({"role": "user", "content": user_input})

    response = agent.invoke({"messages": chat_history})

    ai_message = response["messages"][-1].content

    chat_history.append({"role": "assistant", "content": ai_message})

    return ai_message, chat_history
