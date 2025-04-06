# 导入环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化大模型
from langchain_openai import AzureChatOpenAI
llm = AzureChatOpenAI(azure_endpoint='https://menshen.xdf.cn/', azure_deployment='gpt-4o')

# 生成文本示例
# response = llm.generate("写一篇关于AI技术的简短文章")
# print(response)

# 设置工具
from langchain.agents import load_tools
tools = load_tools(["serpapi"], llm=llm)

# 设置提示模板
from langchain.prompts import PromptTemplate
template = ('''
    '尽你所能用中文回答以下问题。如果能力不够你可以使用以下工具:\n\n'
    '{tools}\n\n
    Use the following format:\n\n'
    'Question: the input question you must answer\n'
    'Thought: you should always think about what to do\n'
    'Action: the action to take, should be one of [{tool_names}]\n'
    'Action Input: the input to the action\n'
    'Observation: the result of the action\n'
    '... (this Thought/Action/Action Input/Observation can repeat N times)\n'
    'Thought: I now know the final answer\n'
    'Final Answer: the final answer to the original input question\n\n'
    'Begin!\n\n'
    'Question: {input}\n'
    'Thought:{agent_scratchpad}' 
    '''
)
prompt = PromptTemplate.from_template(template)

# 初始化Agent
from langchain.agents import create_react_agent
agent = create_react_agent(llm, tools, prompt)

# 构建AgentExecutor
from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               handle_parsing_errors=True,
                               verbose=True)

# 执行AgentExecutor
agent_executor.invoke({"input": "现在需要提出若干个问题，问题使用场景是，新东方老师在开始上课前给家长打电话，家长可能会提出的问题。"
                                "问题几个可能的维度，1.关心教学治疗、2.师资情况、3.孩子学习情况、4.产品具体作用、5.是否能提高成绩，提出对应的家长问题。每个维度提出一个问题，每个问题间要按照以上1-5的顺序提出。"})
