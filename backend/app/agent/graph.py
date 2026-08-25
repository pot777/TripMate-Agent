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

    # 基础信息
    session_id: str

    # 对话历史
    messages: list[dict]

    # 当前旅行状态
    travel_state: dict

    # Agent决策
    decision: AgentAction

    # 工具执行记录
    observations: list[dict]

    # 已执行工具
    executed_calls: list[str]

    # 最终结果
    answer: object

    # 控制字段
    step_count: int



def planner_node(state: AgentState):

    step_count = state.get(
        "step_count",
        0
    )

    if step_count >= 12:

        return {
            "decision": AgentAction(
                action="direct_answer",
                answer="当前处理步骤过多，无法继续完成请求，请重新描述需求。"
            )
        }

    messages = state.get(
        "messages",
        []
    )

    message_context = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )


    travel_state = state.get(
        "travel_state",
        {}
    )
    print("Planner Travel State:")
    print(travel_state)


    current_message = f"""

当前旅行状态：

{travel_state}


历史消息：

{message_context}


决策规则：

1. 如果当前旅行状态中已经存在对应日期的天气信息，
不要再次调用 get_weather。

2. 如果当前旅行状态中已经存在 travel_knowledge，
不要重复调用 retrieve_travel_info。

3. 如果 current_plan 已存在，
用户提出调整需求时，应优先参考已有方案，
避免重新查询已经存在的信息。

4. 如果当前旅行状态中存在 current_plan，
并且用户输入包含：修改、调整、更换、换成、不想去、增加、删除、减少
说明用户希望修改已有方案。
此时优先输出 generate_plan，
不要重新收集完整旅行信息。

"""


    decision = decide_action(
        current_message
    )


    print("Graph Planner Decision:")
    print(decision)


    return {
        "decision": decision,
        "step_count": state.get(
            "step_count",
            0
        ) + 1
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

    if decision.action == "modify_plan":
        return "modify_plan"


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
        state.get(
            "executed_calls",
            []
        )
    )


    if tool_call_key in executed_calls:

        tool_result = {
            "error": "duplicate_tool_call",
            "message": "该工具已使用相同参数执行过，请根据已有结果继续判断。"
        }

    else:

        executed_calls.add(
            tool_call_key
        )

        tool_result = execute_tool(
            decision.tool,
            decision.arguments
        )


    print("Graph Tool Observation:")
    print(tool_result)


    observations = list(
        state.get(
            "observations",
            []
        )
    )


    observations.append(
        {
            "tool": decision.tool,
            "result": tool_result
        }
    )


    messages = list(
        state.get(
            "messages",
            []
        )
    )


    messages.append(
        {
            "role": "tool",
            "content": str(tool_result)
        }
    )


    return {
        "observations": observations,
        "messages": messages,
        "executed_calls": list(executed_calls)
    }



def generate_plan_node(state: AgentState):

    messages = state.get(
        "messages",
        []
    )


    observations = state.get(
        "observations",
        []
    )


    travel_state = state.get(
        "travel_state",
        {}
    )

    current_plan = travel_state.get(
        "current_plan",
        None
    )

    context = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )


    final_prompt = f"""

请根据以下旅行状态、已有旅行方案、用户最新需求和工具结果生成旅行方案。

如果已有current_plan：

这是一次已有方案修改请求，不是重新规划。

必须遵守：

1. 仅修改用户明确提出修改的部分；
2. 未被用户提及的日期(day)必须保持原安排；
3. 不允许调整其他日期的景点顺序；
4. 不允许重新选择未涉及的景点；
5. 必须严格保持用户原始约束：
   - days 不允许改变；
   - budget 不允许降低或修改；
   - 当前旅行预算字段优先级高于已有方案中的预算估算；
   - 如果已有方案预算不足，需要重新调整预算分配，但总预算必须等于用户budget。
6. 如果用户只说“第一天”，只能修改schedule中day=1的内容。


当前旅行状态：

{travel_state}


对话与工具信息：

{context}


工具Observation：

{observations}


已有方案：

{current_plan}

要求：

1. 必须使用所有已经获得的工具信息；
2. 景点信息应体现在每日行程中；
3. 天气信息应影响活动安排，并给出对应出行建议；
4. 不要编造工具未提供的实时信息；
5. 严格输出TravelPlan要求的JSON格式。

"""


    answer = chat_with_llm(
        final_prompt
    )


    print("Graph Final Plan:")
    print(answer)


    return {
        "answer": answer,
        "travel_state": {
            **state.get("travel_state", {}),
            "current_plan": answer.model_dump()
        }
    }


def modify_plan_node(state: AgentState):

    travel_state = state.get(
        "travel_state",
        {}
    )


    current_plan = travel_state.get(
        "current_plan"
    )


    messages = state.get(
        "messages",
        []
    )


    context = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )


    prompt = f"""

你是一个旅行方案修改Agent。

当前已经存在一个旅行方案。

你的任务：
根据用户最新修改要求，
只修改必要部分。

严格规则：

1. 保留没有被用户提及的日期安排。

2. 如果用户说“第一天”，只能修改day=1。

3. 不允许改变：
- 目的地
- 天数
- 用户预算

4. 修改后的结果必须仍然符合TravelPlan JSON格式。


当前旅行状态：

{travel_state}


已有旅行方案：

{current_plan}


用户对话：

{context}


请输出修改后的完整TravelPlan JSON。


"""


    answer = chat_with_llm(
        prompt
    )


    print("Graph Modified Plan:")
    print(answer)


    return {
        "answer": answer,
        "travel_state": {
            **travel_state,
            "current_plan": answer.model_dump()
        }
    }


def direct_answer_node(state: AgentState):

    decision = state["decision"]


    return {
        "answer": decision.answer
    }



def need_information_node(state: AgentState):

    decision = state["decision"]


    return {
        "answer": {
            "status": "need_information",
            "message": decision.message
        }
    }


def update_memory_node(state: AgentState):

    observations = state.get(
        "observations",
        []
    )

    travel_state = dict(
        state.get(
            "travel_state",
            {}
        )
    )

    for obs in observations:

        tool = obs["tool"]
        result = obs["result"]

        # 更新天气
        if tool == "get_weather":

            if result.get("available"):

                weather = travel_state.get(
                    "weather",
                    {}
                )

                date = result["date"]
                weather[date] = result

                travel_state["weather"] = weather

        # 更新旅游知识
        if tool == "retrieve_travel_info":

            if result.get("available"):

                old_knowledge = travel_state.get(
                    "travel_knowledge",
                    []
                )

                new_knowledge = result["knowledge"]

                travel_state["travel_knowledge"] = list(
                    dict.fromkeys(
                        old_knowledge + new_knowledge
                    )
                )


    return {
        "travel_state": travel_state
    }


builder = StateGraph(
    AgentState
)

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "tool",
    tool_node
)

builder.add_node(
    "update_memory",
    update_memory_node
)

builder.add_node(
    "generate_plan",
    generate_plan_node
)

builder.add_node(
    "modify_plan",
    modify_plan_node
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
        "generate_plan": "generate_plan",
        "modify_plan": "modify_plan"
    }
)

builder.add_edge(
    "tool",
    "update_memory"
)

builder.add_edge(
    "update_memory",
    "planner"
)

builder.add_edge(
    "generate_plan",
    END
)

builder.add_edge(
    "modify_plan",
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