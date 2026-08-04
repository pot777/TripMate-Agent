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

## FastAPI作用

FastAPI负责：

1. 接收HTTP请求
2. 调用业务逻辑
3. 返回结果

## 为什么使用Python

AI应用生态主要集中在Python：

- LangChain
- LangGraph
- Transformers
- OpenAI SDK

# TripMate总体架构

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
