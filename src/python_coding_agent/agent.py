import json
import logging
from functools import partial

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
from openai import OpenAI
from openai.types.responses import Response

from .tools import PythonTool

SYSTEM_PROMPT = """
You are a python coding agent.

You MUST follow this process:
1. PLAN:
    - Describe a step-by-step plan.
2. HYPOTHESIS:
    - State assumptions, risks, or approaches.
3. VERIFY:
    - If uncertain, call run_python to test ideas.
4. IMPLEMENT:
    - Present the verified code as your final answer.

Rules:
- Do NOT write final code before VERIFY.
- Use run_python when checking logic or examples.
- Revise plan if verification fails.
"""

class CodingAgent:

    def __init__(
        self,
        model: str,
        client: OpenAI | None = None,
        max_turns: int = 10,
        tool_timeout: int = 30,
        system_prompt: str | None = None,
    ) -> None:
        if client is None:
            load_dotenv()
            client = OpenAI()
        self.client = client
        self.model = model
        self.max_turns = max_turns
        self.tool_timeout = tool_timeout
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.tools = {
            PythonTool.name: partial(PythonTool.func, timeout=tool_timeout)
        }

    def call(
        self,
        user_input: str,
    ) -> Response:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]

        turn = 0
        while turn < self.max_turns:
            turn += 1
            logger.info(f"---- turn {turn} (max: {self.max_turns}) ----")

            logger.info("calling LLM")
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                tools=[PythonTool.definition]
            )
            messages.extend(response.output)

            tool_calls = [o for o in response.output if o.type == "function_call"]
            if len(tool_calls) == 0:
                logger.info("no tool calls, done")
                break

            for tool_call in tool_calls:
                logger.info(f"executing tool: {tool_call.name}")
                args = json.loads(tool_call.arguments)
                func = self.tools[tool_call.name]
                result = func(**args)

                messages.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": result
                })
        
        return response

    def __repr__(self) -> str:
        major_vars = {
            "client": self.client.__class__.__name__,
            "model": self.model,
            "max_turns": self.max_turns,
        }
        var_info = ", ".join([f"{k}={v!r}" for k, v in major_vars.items()])
        return f"{self.__class__.__name__}({var_info})"
