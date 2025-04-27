#!/bin/sh
echo "Installing Notion MCP Server..."
npm install -g @notionhq/notion-mcp-server

echo "Starting Notion MCP Server..."
exec notion-mcp-server --config /usr/src/mcp/mcp.json --port 8000
