import os

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_community.llms import OpenAI
from langchain_community.utilities.serpapi import SerpAPIWrapper

llm = OpenAI(temperature=0)
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
# 定义tools
tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key=serpapi_api_key)
# 初始化agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# 运行agent
agent.run("Who is Elon Mask's girlfriend? What is her current age raised to the 0.43 power?")
