# Python Coding Agent

A simple coding agent that uses OpenAI Responses API to solve programming tasks. The agent follows a structured process (Plan → Hypothesis → Verify → Implement) and can execute Python code to verify its solutions before presenting the final answer.

## Installation

### Install from GitHub (recommended)

```bash
pip install git+https://github.com/coziro/python-coding-agent.git
```

Or using uv:

```bash
uv add git+https://github.com/coziro/python-coding-agent.git
```

### Install from source

```bash
git clone https://github.com/coziro/python-coding-agent.git
cd python-coding-agent
pip install -e .
```

### Set up API key

Create a `.env` file in your project root:

```
OPENAI_API_KEY=your-api-key
```

Or set it as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

## Usage

### Basic usage

```python
from python_coding_agent import CodingAgent

agent = CodingAgent(model="gpt-5-nano")

response = agent.call("Create a function that returns the maximum number from a list")
print(response.output_text)
```

### With custom OpenAI client

If you need custom settings (e.g., custom base URL, timeout, or API key):

```python
from openai import OpenAI
from python_coding_agent import CodingAgent

client = OpenAI(
    api_key="your-api-key",
    base_url="https://your-domain.com/v1",
)
agent = CodingAgent(model="gpt-5-nano", client=client)

response = agent.call("Create a function that returns the maximum number from a list")
print(response.output_text)
```

## Configuration

- `model`: Model name (e.g., "gpt-5-nano")
- `client`: OpenAI client instance (optional, auto-created if not provided)
- `max_turns`: Maximum number of agent turns (default: 10)
- `tool_timeout`: Timeout for Python code execution in seconds (default: 30)
- `system_prompt`: Custom system prompt (optional)
