import textwrap
import tempfile
import subprocess
import sys

TOOL_NAME = "run_python"

TOOL_SCHEMA = {
    "type": "function",
    "name": TOOL_NAME,
    "description": (
        "Execute Python code."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": (
                    "The Python code to execute."
                ),
            },
        },
        "required": ["code"],
        "additionalProperties": False
    },
    "strict": True,
}

def run_python(code: str) -> str:
    code = textwrap.dedent(code)

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(code.encode())
        filename = f.name

    try:
        result = subprocess.run(
            args=[sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=5,  # FIXME
        )
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

TOOL_FUNC = run_python

class PythonTool:
    name = TOOL_NAME
    func = run_python
    schema = TOOL_SCHEMA
