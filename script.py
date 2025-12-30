from auggie_sdk import Auggie
from auggie_sdk.acp import AgentEventListener

# Optional: Create a custom event listener
class MyListener(AgentEventListener):
    def on_agent_message_chunk(self, text: str):
        print(text, end="", flush=True)

    def on_tool_call(self, tool_call_id: str, title: str, kind: str = None, status: str = None):
        print(f"\n[Tool Call] {title} (kind: {kind}, status: {status})")

    def on_tool_response(self, tool_call_id: str, status: str = None, content = None):
        print(f"[Tool Response] Status: {status}")

agent = Auggie(
    # Working directory for the agent (default: current directory)
    workspace_root="/home/sandesh/work/augment_cli",

    # Model to use: "haiku4.5" | "sonnet4.5" | "sonnet4" | "gpt5"
    model="sonnet4.5",

    # Event listener for real-time updates (optional)
    listener=MyListener(),

    # Default timeout in seconds (default: 180)
    timeout=600,

    # API key for authentication (optional, sets AUGMENT_API_TOKEN)
    api_key="e7a146d61375b17dce16fe7c07c3987d0012294fe9a475164142c9e04265a2c9",

    # API URL (optional, sets AUGMENT_API_URL)
    api_url="https://api.augmentcode.com",

    # Rule file paths (optional)
    #rules=["/path/to/rules.md"]
)

# Use the agent
result = agent.run("Your question here", return_type=str)
print(result)