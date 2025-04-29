import os, json, asyncio
import openai
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp.server import MCPServerStdio

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
NOTION_TOKEN   = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DB")

if not openai.api_key:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable")
if not NOTION_TOKEN:
    raise RuntimeError("Please set the NOTION_TOKEN environment variable")
if not NOTION_DATABASE_ID:
    raise RuntimeError("Please set the NOTION_DATABASE_ID environment variable")

# Build the OPENAPI_MCP_HEADERS env var exactly as in your mcp.json
mcp_headers = {
    "Authorization": f"Bearer {os.getenv('NOTION_TOKEN')}",
    "Notion-Version": "2022-06-28"
}
APP_ROOT = os.path.abspath(os.path.dirname(__file__)) 
mcp = MCPServerStdio(
  params={
    "command": "npx",
    "args": [
      "-y",             
      "@notionhq/notion-mcp-server",
      "--config", "./.cursor/mcp.json"
    ],
    # cwd should be wherever your mcp.json lives
    "cwd": APP_ROOT,  
  },
  cache_tools_list=True,
  name="NotionRoadmapBuilderStdio"
)
agent = Agent(
    name="RoadmapBuilder",
    instructions=(
        f"You have access to Notion tools.  Create one page per missing skill in database "
        f"{NOTION_DATABASE_ID}, then append blocks for each learning step."
    ),
    mcp_servers=[mcp],
)

async def main():
    try:
        print("[DEBUG] Starting MCP server and connecting...")
        async with mcp:
            print("[DEBUG] MCP server connected and ready.")

            skill_gap = {
                "missing_skills": ["Docker", "Kubernetes"],
                "roadmap": [
                    {"skill": "Docker", "steps": ["Read docs", "Build sample image"]},
                    {"skill": "Kubernetes", "steps": ["Follow tutorial", "Deploy demo"]},
                ]
            }

            prompt = (
                "Here is a skill-gap analysis:\n"
                f"{json.dumps(skill_gap, indent=2)}\n\n"
                f"Create roadmap entries under database {NOTION_DATABASE_ID}."
            )
            print("[DEBUG] Prompt prepared:")
            print(prompt)

            print("[DEBUG] Sending prompt to agent...")
            result = await Runner.run(starting_agent=agent, input=prompt)
            print("[DEBUG] Agent returned result:")
            print(result)

    except Exception as e:
        print(f"[ERROR] Exception in main: {e}")
    finally:
        print("[DEBUG] Main function completed.")
if __name__ == "__main__":
    asyncio.run(main())
