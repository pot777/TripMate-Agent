import unittest
from unittest.mock import patch

from app.llm import LLMResponseError, chat_with_llm, parse_structured_response
from app.models import AgentAction, TravelPlan


VALID_PLAN = {
    "destination": "重庆",
    "days": 2,
    "budget": 3000,
    "schedule": [
        {
            "day": 1,
            "title": "重庆第一天",
            "activities": ["解放碑"],
            "transportation": "地铁",
            "accommodation_suggestion": "市中心酒店",
        }
    ],
    "food": ["重庆小面"],
    "budget_breakdown": {
        "transportation": 500,
        "accommodation": 1000,
        "food": 500,
        "entertainment": 500,
        "misc": 500,
        "total_estimated": 3000,
    },
}


class LLMResponseTest(unittest.TestCase):

    def test_markdown_json_fence_is_accepted(self):
        content = f"```json\n{__import__('json').dumps(VALID_PLAN, ensure_ascii=False)}\n```"
        plan = parse_structured_response(content, TravelPlan)
        self.assertEqual(plan.destination, "重庆")

    def test_empty_invalid_json_and_validation_errors_are_explicit(self):
        for content in (None, "", "not json", "{}"):
            with self.subTest(content=content):
                with self.assertRaises(LLMResponseError):
                    parse_structured_response(content, TravelPlan)

    def test_plan_format_error_retries_once(self):
        valid_content = __import__('json').dumps(VALID_PLAN, ensure_ascii=False)
        with patch(
            "app.llm._completion_content",
            side_effect=["", valid_content],
        ) as completion:
            plan = chat_with_llm("generate")

        self.assertEqual(plan.destination, "重庆")
        self.assertEqual(completion.call_count, 2)

    def test_network_error_does_not_trigger_manual_retry(self):
        with patch(
            "app.llm._completion_content",
            side_effect=ConnectionError("offline"),
        ) as completion:
            with self.assertRaises(ConnectionError):
                chat_with_llm("generate")

        self.assertEqual(completion.call_count, 1)

    def test_agent_action_schema_validation(self):
        action = parse_structured_response(
            "```json\n{\"action\": \"generate_plan\"}\n```",
            AgentAction,
        )
        self.assertEqual(action.action, "generate_plan")


if __name__ == "__main__":
    unittest.main()
