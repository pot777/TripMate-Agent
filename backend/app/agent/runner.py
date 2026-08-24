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
    session_id: str = "default"
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
        str(answer)
    )

    return answer