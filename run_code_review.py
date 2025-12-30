#!/usr/bin/env python3
"""Run code review on calculate.py using the Auggie SDK"""

from auggie_sdk import Auggie
from auggie_sdk.acp import AgentEventListener

# Optional: Create a custom event listener to see progress
class ReviewListener(AgentEventListener):
    def on_agent_message_chunk(self, text: str):
        print(text, end="", flush=True)

    def on_tool_call(self, tool_call_id: str, title: str, kind: str = None, status: str = None):
        if status == "started":
            print(f"\n[🔧 {title}]", flush=True)

    def on_tool_response(self, tool_call_id: str, status: str = None, content = None):
        pass  # Optional: handle tool responses

# Create agent with your API key
agent = Auggie(
    workspace_root="/home/sandesh/work/augment_cli",
    model="sonnet4",
    listener=ReviewListener(),
    timeout=600,
    api_key="e7a146d61375b17dce16fe7c07c3987d0012294fe9a475164142c9e04265a2c9",
    api_url="https://api.augmentcode.com",
)

# Code review instruction based on your .augment/commands/code-review.md
review_instruction = """You are a specialized code review agent. Review the file calculate.py.

## Review Focus Areas:

- **Bugs & Logic Errors**: Identify bugs, logic errors, edge cases, crash-causing problems.
- **Security Concerns**: Look for potential vulnerabilities, input validation, authentication issues ONLY if the code is security-sensitive
- **Documentation**: Report comments or documentation that is incorrect or inconsistent with the code.
- **API contract violations**
- **Database and schema errors**
- **High Value Typos**: typos that affect correctness, UX-strings, etc.

Review Areas to avoid:

- **Style nags**: e.g. prefer `const` over `let`, prefer template strings, etc.
- **Opinionated suggestions**: e.g. prefer `map` over `forEach`, etc.
- **Low value typos**: e.g. spelling errors in comments, etc.

Please provide a comprehensive code review of calculate.py."""

# Run the code review
print("=" * 80)
print("CODE REVIEW: calculate.py")
print("=" * 80)
print()

result = agent.run(review_instruction, return_type=str)

print("\n")
print("=" * 80)
print("REVIEW COMPLETE")
print("=" * 80)

