# graph.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from ..models import AgentAction
from ..llm import chat_with_llm
from .core import (
    decide_action,
    execute_tool,
    build_tool_call_key
)

class AgentState(TypedDict, total=False):

    session_id: str

    current_message: str

    decision: AgentAction

    tool_result: dict

    final_answer: object

    travel_info_completed: bool

    executed_calls: list[str]

    step_count: int


def planner_node(state: AgentState):

    current_message = state["current_message"]

    decision = decide_action(
        current_message
    )

    print("Graph Planner Decision:")
    print(decision)

    return {
        "decision": decision,
        "step_count": state.get("step_count", 0) + 1
    }


def route_action(state: AgentState):

    decision = state["decision"]

    print("Graph Route:")
    print(decision.action)

    if decision.action == "tool":
        return "tool"

    if decision.action == "need_information":
        return "need_information"

    if decision.action == "generate_plan":
        return "generate_plan"

    if decision.action == "direct_answer":
        return "direct_answer"

    raise ValueError(
        f"Unknown action: {decision.action}"
    )


def tool_node(state: AgentState):

    decision = state["decision"]

    tool_call_key = build_tool_call_key(
        decision.tool,
        decision.arguments
    )

    executed_calls = set(
        state.get("executed_calls", [])
    )

    travel_info_completed = state.get(
        "travel_info_completed",
        False
    )

    if (
        decision.tool == "retrieve_travel_info"
        and travel_info_completed
    ):

        tool_result = {
            "error": "travel_info_already_available",
            "message": "本轮已经获得有效旅游知识，请继续其他必要步骤或生成旅行方案。"
        }

    elif tool_call_key in executed_calls:

        tool_result = {
            "error": "duplicate_tool_call",
            "message": "该工具已使用相同参数执行过，请根据已有结果继续判断。"
        }

    else:

        executed_calls.add(tool_call_key)

        tool_result = execute_tool(
            decision.tool,
            decision.arguments
        )

        if (
            decision.tool == "retrieve_travel_info"
            and isinstance(tool_result, dict)
            and tool_result.get("available") is True
        ):
            travel_info_completed = True

    print("Graph Tool Observation:")
    print(tool_result)

    current_message = state["current_message"]

    current_message += f"""

Tool Observation:

{tool_result}

请根据以上Observation继续判断下一步。

"""

    return {
        "tool_result": tool_result,
        "current_message": current_message,
        "executed_calls": list(executed_calls),
        "travel_info_completed": travel_info_completed
    }


def generate_plan_node(state: AgentState):

    current_message = state["current_message"]

    final_prompt = f"""
请根据以下用户需求和工具Observation生成完整旅行方案：

{current_message}

要求：
1. 必须使用所有已经获得的工具信息；
2. 景点信息应体现在每日行程中；
3. 天气信息应影响活动安排，并给出对应出行建议；
4. 不要编造工具未提供的实时信息；
5. 严格输出TravelPlan要求的JSON格式。
"""

    answer = chat_with_llm(final_prompt)

    print("Graph Final Plan:")
    print(answer)

    return {
        "final_answer": answer
    }


def direct_answer_node(state: AgentState):
    decision = state["decision"]

    return {
        "final_answer": decision.answer
    }


def need_information_node(state: AgentState):

    decision = state["decision"]

    return {
        "final_answer": {
            "status": "need_information",
            "message": decision.message
        }
    }


builder = StateGraph(AgentState)

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "tool",
    tool_node
)

builder.add_node(
    "generate_plan",
    generate_plan_node
)

builder.add_node(
    "direct_answer",
    direct_answer_node
)

builder.add_node(
    "need_information",
    need_information_node
)

builder.add_edge(
    START,
    "planner"
)

builder.add_conditional_edges(
    "planner",
    route_action,
    {
        "tool": "tool",
        "need_information": "need_information",
        "direct_answer": "direct_answer",
        "generate_plan": "generate_plan"
    }
)

builder.add_edge(
    "tool",
    "planner"
)

builder.add_edge(
    "generate_plan",
    END
)

builder.add_edge(
    "need_information",
    END
)

builder.add_edge(
    "direct_answer",
    END
)

graph = builder.compile()

