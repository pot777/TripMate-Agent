# TripMate Agent Learning Notes


## Day1


### LLM应用流程

用户输入
↓
Backend API
↓
Prompt构造
↓
LLM模型
↓
生成Token
↓
返回结果

### FastAPI作用

FastAPI负责：

1. 接收HTTP请求
2. 调用业务逻辑
3. 返回结果

### 为什么使用Python

AI应用生态主要集中在Python：

- LangChain
- LangGraph
- Transformers
- OpenAI SDK

### TripMate总体架构

用户
 |
Vue前端
 |
FastAPI后端
 |
Agent模块
 |
LLM
 |
Tools / RAG / Memory
 |
返回结果

## Day2 - Agent概念预习笔记

### 1. Agent是什么？
Agent = LLM + Planning + Memory + Tools
核心区别：普通LLM是"回答问题"，Agent是"完成任务"。
流程：目标 → 思考 → 规划 → 调用工具 → 观察 → 循环 → 完成

### 2. Tool Calling是什么？
LLM输出结构化指令（JSON），外部系统执行真实操作（API/计算/数据库），结果返回LLM组织回答。
核心：LLM只做决策和生成参数，不执行任何真实操作。

### 3. LangChain是什么？
构建LLM应用的开发框架，封装了Prompt管理、Chain、Tool、Memory等组件。
计划Week 3使用LangGraph实现Agent工作流。

## Day3 - Agent Loop

Agent不是一个新的模型，而是一种应用架构。
Agent是什么？ --Agent是一种利用LLM作为推理核心，通过规划、工具调用和环境反馈完成复杂任务的智能系统。

核心组成：

1. LLM
负责理解需求和决策
2. Tool
提供外部能力
3. Memory
保存历史信息
4. Planning
拆解任务


基本流程：

User Goal
↓
LLM Decision
↓
Action
↓
Tool
↓
Observation
↓
LLM继续决策

当前版本：LLM Application + Tool模块


## Day4 - 当前调用链
main.py
/chat接口
↓
agent.py
run_agent()
↓
agent.py
decide_action()
↓
llm.py
chat_raw()
↓
DeepSeek
返回Action JSON
↓
agent.py
execute_tool()
↓
tools/registry.py
找到工具
↓
tools/weather.py
执行天气查询
↓
agent.py
生成Observation
↓
agent.py
final_prompt
↓
llm.py
chat_with_llm()
↓
DeepSeek
返回旅行JSON
↓
models.py
TravelPlan校验
↓
FastAPI返回


## Day5 - Planner Agent重构

### Agent架构升级

之前版本：

用户输入
↓
简单判断是否调用工具
↓
执行工具
↓
生成答案


当前版本：

用户输入
↓
Agent Planner
↓
生成Action
↓
Tool Registry查找工具
↓
Tool Executor执行
↓
Observation返回
↓
LLM生成最终答案

#### 1. AgentAction结构化输出

新增AgentAction模型，用Pydantic约束LLM决策结果。


LLM不再直接生成回答，而是输出：

{
    "action":"tool",
    "tool":"get_weather",
    "arguments":{
        "city":"成都"
    }
}


程序通过AgentAction解析后执行对应操作。


#### 2. Tool Registry动态管理工具

之前：

Agent代码中直接调用具体工具。


现在：

agent.py通过registry.py统一管理工具：

TOOLS
 |
 |-- get_weather
 |
 |-- search_attractions


每个工具包含：

- 工具名称
- 功能描述
- 参数定义
- 执行函数


新增工具时只需要修改registry，不需要修改Agent核心逻辑。


#### 3. Planner和Executor分离

当前Agent流程：

decide_action()
负责：
- 理解用户需求
- 决定下一步Action


execute_tool()
负责：
- 根据Action中的tool字段查找工具
- 执行对应函数
- 返回Observation


实现了LLM决策和程序执行的职责分离。


## Day6 - Multi-Step Agent

### Agent Loop升级

之前：

User
↓
Planner
↓
Tool
↓
Final

现在：

User
↓
Planner
↓
Tool
↓
Observation
↓
Planner
↓
Tool
↓
Observation
↓
Generate Plan
↓
TravelPlan


### Observation

Tool执行结果不会直接返回用户。

而是作为Observation加入上下文：

current_message
+
Tool Observation

Planner根据Observation继续决定下一步Action。


### generate_plan

Planner负责决策。

TravelPlan属于业务对象。

因此新增：

generate_plan

Planner负责：

什么时候生成旅行方案。

chat_with_llm负责：

生成符合Pydantic的TravelPlan。

实现了：

决策

与

业务对象生成

职责分离。


### MAX_STEPS

Agent Loop增加：

MAX_STEPS

用于限制Agent最大执行次数。

避免LLM重复调用工具导致无限循环。


## Day7 - 天气API接入与Memory升级


### 1. 天气API接入

天气工具从模拟数据升级为高德天气API，实现真实天气查询。

当前支持：
- 当前天气查询
- 指定日期天气查询（受高德未来天气预测范围限制）

遇到的问题：
- 旧API Key类型不匹配，返回USERKEY_PLAT_NOMATCH，更换Web服务Key解决。
- Git Bash和PowerShell Python环境不同，通过虚拟环境检查解释器解决。


### 2. Conversation Memory实现

新增Session Memory模块，通过session_id保存多轮对话。

Memory保存：
- user消息
- tool结果
- assistant回复

实现后Agent可以理解连续任务，例如用户先询问成都天气，再询问游玩5天，Agent可以结合历史上下文理解用户需求。


### 3. Task State Memory实现

新增TravelState保存结构化旅行状态：

{
destination,
days,
budget,
start_date,
weather
}

增加State Extractor，从用户输入中提取旅行信息并更新状态。

例如：

“我想去成都玩5天”

更新：

{
destination:"成都",
days:5
}

同时发现State更新需要采用merge策略，避免LLM返回None覆盖已有信息。


### 4. 当前问题

1. 日期标准化

用户输入“明天出发”“下周一出发”等自然语言日期，需要转换为天气API支持的标准日期格式。


2. 天气查询策略

旅行通常提前规划，而天气API只能预测未来有限日期。

后续需要根据出发日期判断是否调用天气API，较远日期则提供通用建议。


3. Memory持久化

当前Memory基于Python dict，仅适合Demo，后续可升级SQLite/Redis等持久化方案。


## Day8 - State Memory完善与输入规范化

### 1. State Memory接入

之前Agent主要依靠Conversation Memory理解上下文，需要从历史对话中推理旅行状态。

新增Task State Memory，通过extract_state()提取用户输入中的关键信息，并使用update_state()维护结构化旅行状态。

当前状态包含：
- destination
- days
- budget
- start_date

Agent决策时同时读取Conversation Memory和State Memory，提高多轮任务稳定性。


### 2. 日期标准化

用户输入中的日期通常是自然语言表达，无法直接传递给天气API。

增加日期规范化模块，将自然语言日期转换为标准YYYY-MM-DD格式。

支持：
- 今天、明天、后天
- 下周/下下周
- 下个月X号
- X月X号

同时避免LLM直接进行日期计算，将确定性转换逻辑交给代码处理。


### 3. 天气Tool优化

天气工具增加日期范围校验。

调用天气API前判断目标日期是否在未来4天预测范围内。

如果天气不可用，Tool返回available=false，Agent根据Observation继续执行任务。


### 4. 当前优化方向

当前天气查询由Tool内部判断日期有效性。

后续可以考虑让Planner提前判断是否需要调用天气工具，减少无效Tool调用。


## day14 - rag + web_search

Web Search 中文检索能力优化：当前 Web Search fallback 暂时使用 Tavily API，能够满足 Agent 外部知识检索与 RAG fallback 的功能验证，但针对中国境内旅游场景，其中文互联网覆盖、来源质量及简繁体结果仍有进一步优化空间。当前通过统一 search_web() 接口隔离具体搜索服务，后续可根据实际检索效果替换或组合更适合中文旅游场景的 Search Provider，而无需修改 Agent 核心调用逻辑。

TODO：评估中文 Web Search Provider，必要时替换 Tavily；
保持 search_web() 输入输出接口不变，避免影响 Agent 层。

## day16 - 个性化

TODO：未来将 search_attractions 升级为基于 POI API / 结构化景点数据库的候选检索工具，再与 RAG 做 hybrid retrieval。

TODO:
当前自动知识扩充主要由 RAG miss 触发。

后续优化：
引入 knowledge sufficiency 判断，
当已有知识虽然能够命中，但不足以覆盖用户当前需求时，
仍允许触发 Web Search 进行增量知识扩充，
避免单次扩库后知识长期停滞。