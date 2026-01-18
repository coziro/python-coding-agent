# Logging

python-coding-agent uses Python's standard `logging` module. By default, no logs are output.

## Enable logging

```python
import logging

logger = logging.getLogger("python_coding_agent")
logger.setLevel(logging.INFO)
logger.handlers.clear()

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
logger.addHandler(handler)
```

Output:

```
INFO:python_coding_agent.agent:---- turn 1 (max: 10) ----
INFO:python_coding_agent.agent:calling LLM
INFO:python_coding_agent.agent:executing tool: run_python
INFO:python_coding_agent.agent:---- turn 2 (max: 10) ----
INFO:python_coding_agent.agent:calling LLM
INFO:python_coding_agent.agent:no tool calls, done
```

Note: Do not use `logging.basicConfig()` - it enables logs for all packages (openai, httpx, etc.).

To output to a file instead, use `FileHandler`:

```python
handler = logging.FileHandler("agent.log")
```

## Disable logging

```python
logging.getLogger("python_coding_agent").setLevel(logging.WARNING)
```
