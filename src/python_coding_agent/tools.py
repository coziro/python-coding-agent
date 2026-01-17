import textwrap
import tempfile
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    func: Callable[..., str]
    definition: dict


def run_python(code: str, timeout: int = 30) -> str:
    code = textwrap.dedent(code)

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(code.encode())
        filename = f.name

    try:
        result = subprocess.run(
            args=[sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


PYTHON_TOOL_DEFINITION = {
    "type": "function",
    "name": "run_python",
    "description": "Execute Python code and return stdout/stderr.",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute.",
            },
        },
        "required": ["code"],
        "additionalProperties": False,
    },
    "strict": True,
}

PythonTool = Tool(
    name="run_python",
    func=run_python,
    definition=PYTHON_TOOL_DEFINITION,
)
