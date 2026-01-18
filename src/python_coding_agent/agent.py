import json
import logging
from functools import partial

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response

from .tools import PythonTool

logger = logging.getLogger(__name__)


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
            _log_response(response)
            messages.extend(response.output)

            tool_calls = [o for o in response.output if o.type == "function_call"]
            if len(tool_calls) == 0:
                logger.info("no tool calls, done")
                break

            for tool_call in tool_calls:
                logger.info(f"executing tool: {tool_call.name}")
                args = json.loads(tool_call.arguments)
                _log_tool_args(args)
                func = self.tools[tool_call.name]
                result = func(**args)
                _log_tool_result(result)

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


def _log_response(response: Response) -> None:
    logger.debug(f"LLM response: model={response.model}, status={response.status}")
    if response.usage:
        u = response.usage
        logger.debug(f"token usage: in={u.input_tokens}, out={u.output_tokens}")
    logger.debug(f"output types: {[o.type for o in response.output]}")
    if response.output_text:
        logger.debug(f"output_text: {response.output_text[:200]!r}...")
    else:
        logger.debug("output_text: (empty)")


def _log_tool_args(args: dict) -> None:
    if "code" in args:
        code = args["code"]
        if len(code) > 100:
            logger.debug(f"tool args: code={code[:100]!r}...")
        else:
            logger.debug(f"tool args: code={code!r}")
    else:
        logger.debug(f"tool args: {args}")


def _log_tool_result(result: str) -> None:
    if len(result) > 200:
        logger.debug(f"tool result: {result[:200]!r}...")
    else:
        logger.debug(f"tool result: {result!r}")
