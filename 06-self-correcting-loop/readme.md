
Advanced Technique: Using RetryAgentRun
For more robust "hard" failures (e.g., API timeouts or fatal logic errors where the LLM might hallucinate if it just sees text), Agno provides a specific exception mechanism to force a retry loop at the framework level.

You can import and raise RetryAgentRun inside your tool:

Python

from agno.exceptions import RetryAgentRun

def strict_calculator(self, number: int):
    if number % 2 != 0:
        # This stops the agent, feeds the failure back, and forces a retry
        raise RetryAgentRun("That number was odd. You must provide an even number. Try again.")
    return "Number accepted."

    

https://docs.agno.com/reference/tools/retry-agent-run#retryagentrun