# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化大模型
from langchain_openai import AzureChatOpenAI
llm = AzureChatOpenAI(azure_endpoint='https://menshen.xdf.cn/', azure_deployment='gpt-4o')

# 设置工具
from langchain.agents import load_tools
tools = load_tools(["serpapi"], llm=llm)

# 设置计划者和执行者
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)

# 初始化Plan-and-Execute Agent
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
# 运行Agent解决问题
agent.run("现在有一个老师要给家长打电话的工作场景。帮我给出几个家长可能提问的问题，要求家长性格严厉。问题之间要有逻辑连贯性")
