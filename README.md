# Hacker News MCP Server

A Model Context Protocol (MCP) server that provides tools for fetching information from Hacker News.

## Tools

- `get_stories` Fetching (top, new, ask_hn, show_hn) stories
- `get_story_info` Fetching comments associated with a story
- `search_stories` Searching for stories by query
- `get_user_info` Fetching user info

## Example Usage

Use prompts like the following:

```
- Get the top stories of today (will use `get_stories` tool`)
- What does the details of the story today that talks about the future of AI (will use `get_story_info` tool` based on the results of the previous tool)
- What has the user `pg` been up to? (will use `get_user_info` tool)
- What does hackernews say about careers in AI? (will use `search_stories` tool)
```

## Quickstart

### Claude Desktop:

Update the following:

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

With the following for development:

```json
{
  "mcpServers": {
    "mcp-hn": {
      "command": "uv",
      "args": [
        "--directory",
        "<dir_to>/mcp-hn",
        "run",
        "mcp-hn"
      ]
    }
  }
}
```

Or with the following for production:

```json
{
  "mcpServers": {
    "mcp-hn": {
      "command": "uvx",
      "args": ["mcp-hn"]
    }
  }
}
```





