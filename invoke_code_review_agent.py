#!/usr/bin/env python3
"""
Invoke the code review agent to review calculator.py
This script uses the Auggie SDK to invoke your custom code-review agent
"""

from auggie_sdk import Auggie
from auggie_sdk.acp import AgentEventListener
import os

# Create a listener to see the agent's work
class CodeReviewListener(AgentEventListener):
    def on_agent_message_chunk(self, text: str):
        print(text, end="", flush=True)

    def on_tool_call(self, tool_call_id: str, title: str, kind: str = None, status: str = None):
        if status == "started":
            print(f"\n[🔧 Tool: {title}]", flush=True)
    
    def on_tool_response(self, tool_call_id: str, status: str = None, content = None):
        pass

# Get API key from environment
api_key = os.getenv('AUGMENT_API_TOKEN')
if not api_key:
    print("❌ Error: AUGMENT_API_TOKEN environment variable not set")
    print("\nPlease set it with:")
    print("  export AUGMENT_API_TOKEN='your-api-key'")
    exit(1)

# Create agent instance
agent = Auggie(
    workspace_root=os.getcwd(),
    model="sonnet4.5",  # Using the model specified in your code-review agent
    listener=CodeReviewListener(),
    timeout=600,
    api_key=api_key,
    api_url="https://api.augmentcode.com",
)

# Instruction that matches your code-review agent's role
instruction = """You are an agentic code-review AI assistant with access to the developer's codebase through Augment's deep codebase context engine and integrations. You are conducting a comprehensive code review for calculate.py.

## Review Areas to focus on:

- **Potential Bugs**: Identify bugs, logic errors, edge cases, crash-causing problems.
- **Security Concerns**: Look for potential vulnerabilities, input validation, authentication issues ONLY if the code is security-sensitive
- **Documentation**: Report comments or documentation that is incorrect or inconsistent with the code.
- **API contract violations**
- **Database and schema errors**
- **High Value Typos**: typos that affect correctness, UX-strings, etc.

Please review the file calculate.py and provide a comprehensive code review report."""

print("=" * 80)
print("🔍 CODE REVIEW AGENT: calculate.py")
print("=" * 80)
print()

# Run the code review
result = agent.run(instruction, return_type=str)

print("\n")
print("=" * 80)
print("✅ CODE REVIEW COMPLETE")
print("=" * 80)

