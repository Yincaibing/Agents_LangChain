import os

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain_community.utilities import SerpAPIWrapper
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re
from typing import Callable



# 下面是用来将工具集存入到向量库里面，用于工具的检索（可节省token）
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

"""
带工具检索的自定义代理：
当你有很多工具可供选择时，这非常有用。你不能在提示中放置所有工具的描述（由于上下文长度问题)，
因此你动态选择你想要在运行时考虑使用的N个工具。
我们接下来创建一个有点伪需求的例子：
我们将有一个正确的工具（搜索），外加9个假工具。
然后，我们将在提示模板中添加一个步骤，该步骤接受用户输入并检索与查询相关的工具。
"""

# Define which tools the agent can use to answer user queries
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")
search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

search_tool = Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events"
)


def fake_func(inp: str) -> str:
    return "foo"

# 定义假工具集，假设我们有很多种工具可选
fake_tools = [
    Tool(
        name=f"foo-{i}",
        func=fake_func,
        description=f"a silly function that you can use to get more information about the number {i}"
    )
    for i in range(9)
]
ALL_TOOLS = [search_tool] + fake_tools

# 下面是用来将工具集存入到向量库里面，用于工具的检索（可节省token）

# 闯将包含多个Doc对象的数据结构，保存工具信息
docs = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(ALL_TOOLS)]
# 存：存入FAISS向量数据库。from_documents方法就是用来初始化FAISS索引并将其转换为向量存储
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())

# 取：这个操作将vector_store转换为FAISS的检索器格式。类似于jdbc的返回一个db连接对象
# as_retriever方法会返回一个Retriever对象，该对象可以用于在向量存储中执行查找操作。
retriever = vector_store.as_retriever()
def get_tools(query):
    docs = retriever.get_relevant_documents(query)
    return [ALL_TOOLS[d.metadata["index"]] for d in docs]

# 测试检索器
get_tools("what's the weather?")


# 设置提示词模板
template = """Answer the following questions as best you can,
but speaking as a pirate might speak. You have access to the following tools:
{tools}
Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

Question: {input}
{agent_scratchpad}"""

# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    ############## NEW ######################
    # The list of tools available
    tools_getter: Callable

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        ############## NEW ######################
        tools = self.tools_getter(kwargs["input"])
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
        return self.template.format(**kwargs)


prompt = CustomPromptTemplate(
    template=template,
    tools_getter=get_tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


output_parser = CustomOutputParser()

llm = OpenAI(temperature=0)
# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)
tools = get_tools("whats the weather?")
tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names
)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
agent_executor.run("What's the weather in Chengdu today?")
