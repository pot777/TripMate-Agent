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