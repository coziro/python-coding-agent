# Python Coding Agent

A simple coding agent that uses OpenAI Responses API to solve programming tasks. The agent follows a structured process (Plan → Hypothesis → Verify → Implement) and can execute Python code to verify its solutions before presenting the final answer.

## Installation

```bash
pip install -e .
```

## Usage

```python
from openai import OpenAI
from python_coding_agent import CodingAgent

client = OpenAI()
agent = CodingAgent(
    client=client,
    model="gpt-4o",
    max_turns=10,
)

response = agent.call("Create a function that returns the maximum number from a list")
print(response.output_text)
```

## Configuration

- `client`: OpenAI client instance
- `model`: Model name (e.g., "gpt-4o")
- `max_turns`: Maximum number of agent turns (default: 10)
- `tool_timeout`: Timeout for Python code execution in seconds (default: 30)
- `system_prompt`: Custom system prompt (optional)
