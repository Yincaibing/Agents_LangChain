from langchain_community.retrievers import BreebsRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model_name="gpt-4")

retriever = BreebsRetriever(
    breeb_key="https://www.langchain.com.cn/use_cases/agent_simulations",
    # api_key="DATABERRY_API_KEY", # optional if datastore is public
    # top_k=10 # optional
)

retriever.get_relevant_documents("What is 代理模拟?")
