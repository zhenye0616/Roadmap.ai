import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
load_dotenv() 
print("NOTION_DB:", os.getenv("NOTION_DB"))
  # you can temporarily log this
print("NOTION_TOKEN:", os.getenv("NOTION_TOKEN"))

# Ensure env vars are set
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB    = os.getenv("NOTION_DB")
if not NOTION_TOKEN or not NOTION_DB:
    raise RuntimeError("Please set NOTION_TOKEN and NOTION_DB environment variables.")

notion = Client(auth=NOTION_TOKEN)

resp = notion.search(
    **{
        "query": "",
        "filter": {"value": "database", "property": "object"}
    }
)
print("Databases visible to integration:")
for db in resp["results"]:
    title = db["title"][0]["plain_text"] if db["title"] else "(no title)"
    print(f" • {db['id']}  ‹{title}›")
    
def create_user_page(user_id: str, skills: list[str]):
    # 1) Define the page properties to match your database schema:
    properties = {
        "Name": {
            "title": [
                {
                    "type": "text",
                    "text": {"content": user_id}
                }
            ]
        },
        # e.g. if your DB has a multi-select or text field called "Skills":
        "Skills": {
            "multi_select": [{"name": skill} for skill in skills]
        }
    }

    # 2) Build valid block objects for 'children'
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"{user_id}'s Skill Gap Report"
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "✅ Skills identified: " + ", ".join(skills)
                        }
                    }
                ]
            }
        }
    ]

    # 3) Call the API with a parent, properties, and properly formed children
    return notion.pages.create(
        parent={"database_id": NOTION_DB},
        properties=properties,
        children=children
    )
