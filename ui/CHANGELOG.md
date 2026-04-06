# Changelog

## [Unreleased] - 2026-03-20

### Added

#### Backend Server (`backend/server.py`)
- Created standalone FastAPI server to connect NAT UI to LangChain deepagents framework
- Integrated `LocalShellBackend` from deepagents for filesystem and shell tool access
- Implemented OpenAI-compatible API endpoints:
  - `GET /health` - Health check endpoint
  - `POST /generate` - Non-streaming generate endpoint
  - `POST /generate/stream` - Streaming generate with SSE
  - `POST /chat` - Non-streaming chat endpoint
  - `POST /chat/stream` - Streaming chat with intermediate steps
  - `POST /v1/chat/completions` - OpenAI v1 compatible endpoint
  - `GET /mcp/client/tool/list` - MCP tools list (empty placeholder)
  - `WS /websocket` - WebSocket endpoint for real-time chat

#### Intermediate Steps Display
- Added tool formatting helpers with icons and display names:
  - `ls` -> "List Directory"
  - `read_file` -> "Read File"
  - `write_file` / `edit_file` -> "Write/Edit File"
  - `execute` -> "Shell Command"
  - `glob` -> "Find Files"
  - `grep` -> "Search Content"
  - `task` -> "Subagent Task"
  - `write_todos` -> "Update Todos"

- Implemented `format_tool_call()` function:
  - Formats tool calls with icons and markdown payloads
  - Shows command arguments in code blocks
  - File paths displayed with backticks

- Implemented `format_tool_result()` function:
  - Formats tool results with syntax highlighting
  - Directory listings as bullet points
  - File contents in code blocks
  - Command output in code blocks
  - Automatic truncation for long outputs (1500 chars)

- Integrated `intermediate_data:` SSE protocol for streaming tool steps to frontend

#### Environment Configuration
- Created `backend/.env` for Anthropic API key storage

### Technical Details

#### Message Conversion
- Added `convert_to_langchain_messages()` to handle various message formats:
  - Dict with role/content
  - String messages
  - LangChain BaseMessage objects
  - Objects with content attribute

#### Streaming Architecture
- Streams tool calls with `status: "in_progress"`
- Streams tool results with `status: "complete"`
- Handles LangGraph's `Overwrite` wrapper objects
- Tracks `last_tool_name` for result formatting
- Incremental content streaming (only sends new content)

### Dependencies
- `deepagents` - LangChain agent framework
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable loading
- `langchain-core` - Message types

### Running the Server

```bash
# Start backend (port 8000)
source .venv/bin/activate
python server.py

# Start frontend (port 3000)
cd ui && npm run dev
```

### Configuration

The backend connects to:
- Model: Configurable via environment
- Root directory: Project root
- Virtual mode: disabled (real filesystem access)
