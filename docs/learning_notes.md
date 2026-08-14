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

## day16 - 个性化检索与 LangGraph 重构

TODO：未来将 search_attractions 升级为基于 POI API / 结构化景点数据库的候选检索工具，再与 RAG 做 hybrid retrieval。

TODO:
当前自动知识扩充主要由 RAG miss 触发。

后续优化：
引入 knowledge sufficiency 判断，
当已有知识虽然能够命中，但不足以覆盖用户当前需求时，
仍允许触发 Web Search 进行增量知识扩充，
避免单次扩库后知识长期停滞。

### Agent 工具调用去重

问题：
仅在 Prompt 中要求 Agent “不要重复调用工具”属于软约束，LLM 仍可能因为 query 表述变化而重复执行语义相同的工具任务，例如多次调用 retrieve_travel_info。

改进：
在 Agent Runtime 中增加工具调用状态控制：

- executed_calls：记录本轮已经执行的具体工具调用，通过 tool name + arguments 生成唯一 key，阻止完全相同的工具调用重复执行。
- completed_tasks：记录已经完成的信息获取任务。例如 retrieve_travel_info 返回 available=true 后，将 travel_info 标记为已完成，之后即使 LLM 使用不同 query 再次请求 RAG，也不再实际执行。

总结：
Prompt 负责告诉 Agent “应该怎么做”，Runtime Guard 负责保证 Agent “不能违反关键执行约束”。对于工具去重、最大循环次数等确定性约束，不应完全依赖 LLM。

### LangGraph Agent Runtime

LangGraph 是什么：LangGraph 是面向有状态 Agent 工作流的图编排框架。它本身不负责替代 LLM、Tool、RAG 或 Memory，而是负责组织这些模块之间的执行流程。相比原先在 `run_agent()` 中通过 `for + if + continue` 手动控制 Agent 循环，LangGraph 将 Agent Runtime 显式表示为 Node、Edge 和 State。

为什么引入 LangGraph：原有 Agent 已经具备 Planner、Tool Calling、RAG、Web Search、Memory 和计划生成能力，但所有流程控制都集中在 `run_agent()` 中。随着 Action 和异常分支增加，继续使用手写循环会导致控制逻辑越来越复杂。因此保留已有业务模块，只将 Agent 的流程编排层迁移到 LangGraph。

Node：Node 表示工作流中的一个处理步骤，本质上是接收当前 Graph State 并返回部分状态更新的函数。当前项目主要包含：
- `planner`：调用 LLM 判断下一步 Action；
- `tool`：执行工具并保存 Observation；
- `generate_plan`：根据用户状态和工具结果生成结构化 TravelPlan；
- `direct_answer`：处理无需生成完整旅行计划的普通问答；
- `need_information`：返回缺失信息提示。

Edge：Edge 决定 Node 之间的执行方向。普通 Edge 表示固定跳转，例如 `tool -> planner`；Conditional Edge 根据当前 State 动态决定下一节点，例如 `planner` 根据 `AgentAction.action` 分流到 `tool`、`need_information`、`direct_answer` 或 `generate_plan`。

Graph State：Graph State 是一次 Graph 执行过程中各 Node 共享的数据载体。当前使用 `AgentState(TypedDict)` 保存 `current_message`、`decision`、`tool_result`、`final_answer`、`executed_calls`、`travel_info_completed`、`step_count` 等运行时信息。Node 不需要手动互相调用，而是通过读取和更新 State 协作。

Graph State 与 TravelState 的区别：`TravelState` 保存用户跨轮对话中的旅行需求，例如 destination、days、budget、start_date、travelers、preferences、interests；`AgentState` 保存一次 Agent Graph 执行过程中的运行时状态。前者属于业务 Memory，后者属于 Workflow Runtime State，两者职责不同。

当前 Graph 主流程：

START
→ planner
→ route_action
→ tool → planner（循环）
→ need_information → END
→ direct_answer → END
→ generate_plan → END

为什么 tool 要回到 planner：工具只负责提供 Observation，并不能自行决定任务是否完成。执行 Tool 后将结果追加到 `current_message`，再返回 planner，由 LLM 根据新信息判断是否继续调用其他工具、直接回答或生成计划，从而形成 Agent 的 observe → reason → act 循环。

为什么 generate_plan 和 direct_answer 分开：`generate_plan` 用于完整旅行规划，需要调用 `chat_with_llm()` 并按照 `TravelPlan` 输出结构化结果；`direct_answer` 用于天气等简单问题，Planner 已经产生最终自然语言回答，不需要再进行一次计划生成。原先名为 `final` 容易与 Graph 的 END 混淆，因此改名为 `direct_answer`。

为什么 Node 后还需要 END：Node 表示“执行什么业务逻辑”，END 表示“Graph 执行到这里正式终止”。例如 `generate_plan` 负责生成结果，而 `generate_plan -> END` 表示生成完成后工作流结束。二者属于不同层次，不能简单视为同一个概念。

迁移原则：没有重写已有 Tool、RAG、Memory 和 LLM 逻辑，而是将原有 `decide_action()`、`execute_tool()`、`build_tool_call_key()` 等能力保留在 `agent/core.py`，由 `graph.py` 负责工作流编排，`runner.py` 负责连接 FastAPI/Memory 与 Graph。最终目录职责为：
- `agent/core.py`：Agent 基础能力与 Planner；
- `agent/graph.py`：LangGraph Node、Edge、State 和 Graph；
- `agent/runner.py`：Agent 对外运行入口。

日期参数边界：在真实 Graph 测试中发现 Planner 可能直接向 `get_weather` 传入“明天”等自然语言日期，而 TravelState 中的日期标准化无法覆盖 Tool 参数。因此将日期标准化同时放到 Weather Tool 边界，使 `get_weather()` 自身能够处理自然语言日期。这个问题说明 Tool 应尽量具备稳定、明确的输入契约，而不能假设上游 LLM 一定传入完全规范化参数。

当前尚未引入 LangGraph Checkpoint/Persistence。现阶段 Graph State 主要用于单次 Agent Runtime，跨轮用户旅行信息仍由项目原有 Memory/TravelState 管理。后续再根据实际需求决定是否使用 LangGraph Checkpointer 统一或增强状态持久化。