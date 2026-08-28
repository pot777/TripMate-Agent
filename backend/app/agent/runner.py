import re

from .graph import graph, AgentState

from ..memory.store import (
    add_message,
    get_history
)

from ..memory.extractor import extract_state

from ..memory.state import (
    get_state,
    update_state
)


def run_graph(
    message: str,
    session_id: str = "default",
    include_trace: bool = False
):

    # 1. 保存当前用户消息
    add_message(
        session_id,
        "user",
        message
    )

    # 2. 从当前用户输入提取结构化旅行状态
    extracted = extract_state(
        message
    )

    # 3. 合并到当前 Session 的 TravelState
    update_state(
        session_id,
        **extracted
    )

    # 4. 获取 Conversation Memory 和 TravelState
    history = get_history(
        session_id
    )

    travel_state = get_state(
        session_id
    )
    had_current_plan = bool(travel_state.current_plan)

    print("Travel State:")
    print(travel_state)

    # 5. 构造 LangGraph 初始状态
    initial_state = {
        "session_id": session_id,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "travel_state": travel_state.model_dump(),
        "observations": [],
        "executed_calls": [],
        "step_count": 0
    }

    # 6. 启动 Graph
    result = graph.invoke(
        initial_state
    )

    # 7. 将Graph中的最新travel_state同步回Memory
    update_state(
        session_id,
        **result["travel_state"]
    )

    # 8. 所有结束路径都统一从 answer 取结果
    answer = result["answer"]

    # 9. 保存 Assistant 回复
    add_message(
        session_id,
        "assistant",
        answer
    )

    trace = _build_trace(
        message=message,
        had_current_plan=had_current_plan,
        result=result,
        answer=answer
    )

    return (answer, trace) if include_trace else answer


def run_graph_stream(
    message: str,
    session_id: str = "default"
):
    """Run the existing graph and yield safe, user-facing events as nodes finish."""
    add_message(session_id, "user", message)

    extracted = extract_state(message)
    update_state(session_id, **extracted)

    # Keep the same memory access and initial state used by run_graph.
    get_history(session_id)
    travel_state = get_state(session_id)
    had_current_plan = bool(travel_state.current_plan)

    initial_state = {
        "session_id": session_id,
        "messages": [{"role": "user", "content": message}],
        "travel_state": travel_state.model_dump(),
        "observations": [],
        "executed_calls": [],
        "step_count": 0
    }

    if not had_current_plan:
        yield {
            "event": "trace",
            "data": _trace_event("state", "state_extraction", "已识别旅行需求")
        }

    result = dict(initial_state)
    seen_tools = set()
    modification_identified = False
    state_identified = not had_current_plan
    knowledge_unavailable = False

    for update_batch in graph.stream(initial_state, stream_mode="updates"):
        for node_name, update in update_batch.items():
            if not isinstance(update, dict):
                continue
            result.update(update)

            if node_name == "planner":
                action = _decision_action(update)
                if action == "modify_plan" and had_current_plan and not modification_identified:
                    modification_identified = True
                    state_identified = True
                    yield {
                        "event": "trace",
                        "data": _trace_event("state", "current_plan", "已读取当前旅行方案")
                    }
                    yield {
                        "event": "trace",
                        "data": _trace_event("state", "state_extraction", "已识别修改需求")
                    }
                elif had_current_plan and not state_identified:
                    state_identified = True
                    yield {
                        "event": "trace",
                        "data": _trace_event("state", "state_extraction", "已识别旅行需求")
                    }

            elif node_name == "tool":
                observations = update.get("observations", [])
                if not observations:
                    continue
                observation = observations[-1]
                tool_name = observation.get("tool")
                tool_result = observation.get("result", {})
                if tool_name in seen_tools:
                    continue
                seen_tools.add(tool_name)

                event = None
                if tool_name == "get_weather":
                    city = _result_value(tool_result, "city")
                    label = f"已查询{city}天气" if city else "已完成天气查询"
                    event = _trace_event("tool", tool_name, label)
                elif tool_name == "retrieve_travel_info":
                    available = bool(_result_value(tool_result, "available", False))
                    knowledge_unavailable = not available
                    if available:
                        event = _trace_event("tool", tool_name, "已检索旅游信息")
                elif tool_name == "search_web":
                    label = (
                        "知识库未覆盖，已补充网络旅游信息"
                        if knowledge_unavailable
                        else "已补充网络旅游信息"
                    )
                    event = _trace_event("tool", tool_name, label)

                if event:
                    yield {"event": "trace", "data": event}

            elif node_name == "generate_plan":
                answer = update.get("answer")
                days = _plan_days(answer)
                label = f"已生成{days}日旅行方案" if days else "已生成旅行方案"
                yield {
                    "event": "trace",
                    "data": _trace_event("plan", node_name, label)
                }
            elif node_name == "modify_plan":
                day = _mentioned_day(message)
                label = f"已更新第{day}天行程" if day else "已更新旅行方案"
                yield {
                    "event": "trace",
                    "data": _trace_event("plan", node_name, label)
                }
            elif node_name == "need_information":
                yield {
                    "event": "trace",
                    "data": _trace_event("information", node_name, "需要补充旅行信息")
                }
            elif node_name == "direct_answer" and not seen_tools:
                yield {
                    "event": "trace",
                    "data": _trace_event("answer", node_name, "已完成查询")
                }

    # Preserve the existing persistence order before exposing the final result.
    update_state(session_id, **result["travel_state"])
    answer = result["answer"]
    add_message(session_id, "assistant", answer)

    yield {
        "event": "result",
        "data": {
            "type": "result",
            "answer": answer.model_dump() if hasattr(answer, "model_dump") else answer
        }
    }


def _trace_event(event_type, name, message):
    return {
        "type": event_type,
        "name": name,
        "status": "completed",
        "message": message
    }


def _decision_action(result):
    decision = result.get("decision")
    if isinstance(decision, dict):
        return decision.get("action")
    return getattr(decision, "action", None)


def _result_value(result, key, default=None):
    if isinstance(result, dict):
        return result.get(key, default)
    return getattr(result, key, default)


def _mentioned_day(message):
    match = re.search(r"第\s*(\d+|[一二三四五六七八九十]+)\s*天", message)
    if not match:
        return None

    value = match.group(1)
    if value.isdigit():
        return int(value)

    chinese_numbers = {
        "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9, "十": 10
    }
    return chinese_numbers.get(value)


def _plan_days(answer):
    if isinstance(answer, dict):
        return answer.get("days")
    return getattr(answer, "days", None)


def _build_trace(message, had_current_plan, result, answer):
    """Build user-facing execution summaries without exposing model reasoning."""
    action = _decision_action(result)
    observations = result.get("observations", []) or []
    trace = []

    if action == "modify_plan" and had_current_plan:
        trace.append(_trace_event("state", "current_plan", "已读取当前旅行方案"))
        trace.append(_trace_event("state", "state_extraction", "已识别修改需求"))
    elif action in {"generate_plan", "need_information"}:
        trace.append(_trace_event("state", "state_extraction", "已识别旅行需求"))

    seen_tools = set()
    knowledge_unavailable = False
    for observation in observations:
        tool_name = observation.get("tool") if isinstance(observation, dict) else None
        tool_result = observation.get("result", {}) if isinstance(observation, dict) else {}
        if tool_name in seen_tools:
            continue
        seen_tools.add(tool_name)

        if tool_name == "get_weather":
            city = _result_value(tool_result, "city")
            label = f"已查询{city}天气" if city else "已完成天气查询"
            trace.append(_trace_event("tool", tool_name, label))
        elif tool_name == "retrieve_travel_info":
            available = bool(_result_value(tool_result, "available", False))
            knowledge_unavailable = not available
            if available:
                trace.append(_trace_event("tool", tool_name, "已检索旅游信息"))
        elif tool_name == "search_web":
            label = (
                "知识库未覆盖，已补充网络旅游信息"
                if knowledge_unavailable
                else "已补充网络旅游信息"
            )
            trace.append(_trace_event("tool", tool_name, label))

    if action == "generate_plan":
        days = _plan_days(answer)
        label = f"已生成{days}日旅行方案" if days else "已生成旅行方案"
        trace.append(_trace_event("plan", action, label))
    elif action == "modify_plan":
        day = _mentioned_day(message)
        label = f"已更新第{day}天行程" if day else "已更新旅行方案"
        trace.append(_trace_event("plan", action, label))
    elif action == "need_information":
        trace.append(_trace_event("information", action, "需要补充旅行信息"))
    elif action == "direct_answer" and not trace:
        trace.append(_trace_event("answer", action, "已完成查询"))

    return trace
