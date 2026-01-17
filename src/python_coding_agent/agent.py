from .tools import PythonTool
import json

TOOLS = {
    PythonTool.name: PythonTool.func,
}

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
    - Only after verification, write the final code.

Rules:
- Do NOT write final code before VERIFY.
- Use run_python when checking logic or examples.
- Revise plan if verification fails.
"""

class CodingAgent:

    def __init__(
        self,
        client,
        model,
        max_turns: int = 10,
    ):
        self.client = client
        self.model = model
        self.max_turns = max_turns

    def call(
        self,
        input: str,
    ):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input}
        ]

        turn = 0
        while turn < self.max_turns:
            print(f"turn: {turn}")
            turn += 1

            print("call llm")
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                tools=[PythonTool.schema]
            )
            messages.extend(response.output)

            tool_calls = [o for o in response.output if o.type == "function_call"]
            if len(tool_calls) == 0:
                break

            for tool_call in tool_calls:
                print("execute function")
                args = json.loads(tool_call.arguments)
                func = TOOLS[tool_call.name]
                result = func(**args)

                print("add function result to messages")
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
