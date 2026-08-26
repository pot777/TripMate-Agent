import importlib
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


TEST_DIRECTORY = tempfile.TemporaryDirectory()
TEST_DATABASE = Path(TEST_DIRECTORY.name) / "tripmate-test.db"
os.environ["TRIPMATE_DATABASE_URL"] = f"sqlite:///{TEST_DATABASE.as_posix()}"

from app.db.database import engine, init_db  # noqa: E402
from app.memory.state import get_state, update_state  # noqa: E402
from app.memory.store import (  # noqa: E402
    add_message,
    get_conversation_detail,
    get_history,
    list_conversations,
)


class PersistenceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    @classmethod
    def tearDownClass(cls):
        engine.dispose()
        TEST_DIRECTORY.cleanup()

    def test_state_plan_messages_and_runner_survive_new_connections(self):
        conversation_id = "persistence-case"
        plan = {
            "destination": "哈尔滨",
            "days": 3,
            "budget": 5000,
            "schedule": [
                {
                    "day": day,
                    "title": f"哈尔滨第{day}天",
                    "activities": [f"原行程{day}"],
                    "transportation": "公共交通",
                    "accommodation_suggestion": "市中心酒店",
                }
                for day in range(1, 4)
            ],
            "food": [],
            "budget_breakdown": {
                "transportation": 1000,
                "accommodation": 1500,
                "food": 1000,
                "entertainment": 1000,
                "misc": 500,
                "total_estimated": 5000,
            },
        }

        add_message(conversation_id, "user", "我想去哈尔滨玩3天，预算5000，明天出发")
        update_state(
            conversation_id,
            destination="哈尔滨",
            days=3,
            budget=5000,
            start_date="明天",
            travelers=["父母"],
            preferences=["轻松"],
            current_plan=plan,
        )
        add_message(conversation_id, "assistant", plan)

        engine.dispose()

        restored = get_state(conversation_id)
        self.assertEqual(restored.destination, "哈尔滨")
        self.assertEqual(restored.days, 3)
        self.assertEqual(restored.budget, 5000)
        self.assertEqual(restored.current_plan, plan)

        update_state(
            conversation_id,
            travelers=["父母", "孩子"],
            preferences=["轻松", "少走路"],
            destination=None,
        )
        merged = get_state(conversation_id)
        self.assertEqual(merged.travelers, ["父母", "孩子"])
        self.assertEqual(merged.preferences, ["轻松", "少走路"])
        self.assertEqual(merged.destination, "哈尔滨")
        self.assertEqual(merged.current_plan, plan)

        manually_edited_plan = json.loads(json.dumps(plan, ensure_ascii=False))
        manually_edited_plan["schedule"][1]["activities"] = ["中央大街轻松散步"]
        update_state(conversation_id, current_plan=manually_edited_plan)
        engine.dispose()
        self.assertEqual(get_state(conversation_id).current_plan, manually_edited_plan)

        captured_state = {}

        class FakeGraph:
            def invoke(self, initial_state):
                captured_state.update(initial_state)
                return {
                    "travel_state": initial_state["travel_state"],
                    "answer": "已根据原方案调整第二天行程",
                }

        graph_module = types.ModuleType("app.agent.graph")
        graph_module.graph = FakeGraph()
        graph_module.AgentState = dict
        extractor_module = types.ModuleType("app.memory.extractor")
        extractor_module.extract_state = lambda message: {}

        with patch.dict(
            sys.modules,
            {
                "app.agent.graph": graph_module,
                "app.memory.extractor": extractor_module,
            },
        ):
            sys.modules.pop("app.agent.runner", None)
            runner = importlib.import_module("app.agent.runner")
            runner.run_graph("第二天换一个轻松一点的地方", conversation_id)

        self.assertEqual(captured_state["travel_state"]["current_plan"], manually_edited_plan)

        history = get_history(conversation_id)
        self.assertEqual(len(history), 4)
        self.assertEqual(history[-2]["content"], "第二天换一个轻松一点的地方")

        conversations = list_conversations()
        self.assertEqual(conversations[0]["id"], conversation_id)
        self.assertEqual(conversations[0]["title"], "哈尔滨3日游")
        self.assertEqual(conversations[0]["preview"], "第二天换一个轻松一点的地方")

        detail = get_conversation_detail(conversation_id)
        self.assertIsNotNone(detail)
        self.assertEqual(detail["current_plan"], manually_edited_plan)
        self.assertEqual(len(detail["messages"]), 4)
        self.assertEqual(detail["messages"][1]["content"], plan)

        add_message(
            "message-format-case",
            "assistant",
            {
                "status": "need_information",
                "message": "请补充旅行天数和预算",
            },
        )
        add_message(
            "legacy-message-case",
            "assistant",
            "{'status': 'need_information', 'message': '请问计划玩几天？'}",
        )

        json_detail = get_conversation_detail("message-format-case")
        legacy_detail = get_conversation_detail("legacy-message-case")
        self.assertEqual(
            json_detail["messages"][0]["content"],
            {
                "status": "need_information",
                "message": "请补充旅行天数和预算",
            },
        )
        self.assertEqual(
            legacy_detail["messages"][0]["content"],
            {
                "status": "need_information",
                "message": "请问计划玩几天？",
            },
        )


if __name__ == "__main__":
    unittest.main()
