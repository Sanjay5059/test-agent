import streamlit as st

from agents.basic_agent import run_basic_agent
from agents.memory_agent import run_memory_agent
from agents.multi_tool_agent import run_multi_tool_agent
from agents.planner_agent import run_planner_agent
from agents.rag_agent import run_rag_agent
from agents.reasoning_agent import run_reasoning_agent

st.set_page_config(page_title="Weather Agent", page_icon="🌤", layout="wide")
st.title("Weather Agent")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
    )
    agent_type = st.radio(
        "Agent",
        [
            "Basic Agent",
            "Memory Agent",
            "Multi-Tool Agent",
            "Planner Agent",
            "RAG Agent",
            "Reasoning Agent",
        ],
    )
    st.divider()
    st.caption("Select an agent, enter your query, and click Run.")

# Session state
if "memory_history" not in st.session_state:
    st.session_state.memory_history = []
if "rag_history" not in st.session_state:
    st.session_state.rag_history = []

descriptions = {
    "Basic Agent": "Fetches current weather for a city.",
    "Memory Agent": "Multi-turn chat using weather + calculator tools.",
    "Multi-Tool Agent": "Single-turn query using weather + calculator tools.",
    "Planner Agent": "Creates a jogging plan based on current weather.",
    "RAG Agent": "Multi-turn chat grounded in the weather knowledge base.",
    "Reasoning Agent": "Step-by-step reasoning: weather to jogging advice.",
}
st.info(f"**{agent_type}** - {descriptions[agent_type]}")

if agent_type == "Basic Agent":
    city = st.text_input("City", placeholder="e.g. London")
    if st.button("Get Weather", type="primary") and city:
        with st.spinner("Fetching weather..."):
            result = run_basic_agent(city=city, model=model)
        st.markdown("### Result")
        st.write(result)

elif agent_type == "Memory Agent":
    if st.button("Clear History"):
        st.session_state.memory_history = []
        st.rerun()
    for msg in st.session_state.memory_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    user_input = st.chat_input("Ask something...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.spinner("Thinking..."):
            reply, st.session_state.memory_history = run_memory_agent(
                chat_history=st.session_state.memory_history,
                user_input=user_input,
                model=model,
            )
        with st.chat_message("assistant"):
            st.write(reply)

elif agent_type == "Multi-Tool Agent":
    query = st.text_area("Query", placeholder="e.g. What is the weather in Tokyo and convert 25C to F?")
    if st.button("Run", type="primary") and query:
        with st.spinner("Running..."):
            result = run_multi_tool_agent(query=query, model=model)
        st.markdown("### Result")
        st.write(result)

elif agent_type == "Planner Agent":
    query = st.text_area("Query", placeholder="e.g. Should I go jogging in Singapore today?")
    if st.button("Create Plan", type="primary") and query:
        with st.spinner("Planning..."):
            result = run_planner_agent(query=query, model=model)
        st.markdown("### Jogging Plan")
        st.write(result)

elif agent_type == "RAG Agent":
    if st.button("Clear History"):
        st.session_state.rag_history = []
        st.rerun()
    for msg in st.session_state.rag_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    user_input = st.chat_input("Ask something from the knowledge base...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.spinner("Searching knowledge base..."):
            reply, st.session_state.rag_history = run_rag_agent(
                chat_history=st.session_state.rag_history,
                user_input=user_input,
                model=model,
            )
        with st.chat_message("assistant"):
            st.write(reply)

elif agent_type == "Reasoning Agent":
    query = st.text_area("Query", placeholder="e.g. Is it good weather for jogging in Paris?")
    if st.button("Analyze", type="primary") and query:
        with st.spinner("Reasoning..."):
            result = run_reasoning_agent(query=query, model=model)
        st.markdown("### Analysis")
        st.write(result)
