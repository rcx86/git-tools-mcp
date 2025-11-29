# Git Tools MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with local Git repositories. This server allows LLMs to inspect commit history, diffs, and file changes in your local projects.

This is a personal project for my internal use-case.

## Installation

You can install the package using `uv` or `pip`:

```bash
uv pip install .
# or
pip install .
```

## Usage

### Running the Server

The server can be run in two modes:

1. **Stdio Mode** (Default):
   ```bash
   git-tools-mcp
   ```
   This is the standard mode for use with MCP clients (like Claude Desktop or other LLM interfaces).

2. **HTTP Mode** (SSE):
   ```bash
   git-tools-mcp --http --port 8000
   ```
   This runs the server over HTTP using Server-Sent Events (SSE).

### Available Tools

The server exposes the following tools:

- **`git_get_commit_history(n: int = 10, cwd: Optional[str] = None)`**
  - Retrieves the last `n` commit hashes.
  - `n`: Number of commits to retrieve (default: 10).
  - `cwd`: Working directory (optional).

- **`git_get_commit_message(commit_hash: str, cwd: Optional[str] = None)`**
  - Gets the commit message for a specific commit hash.
  - `commit_hash`: The hash of the commit.
  - `cwd`: Working directory (optional).

- **`git_get_commit_diff(commit_hash: str, cwd: Optional[str] = None)`**
  - Gets the diff for a specific commit.
  - `commit_hash`: The hash of the commit.
  - `cwd`: Working directory (optional).

- **`git_get_changed_files(commit_hash: str, cwd: Optional[str] = None)`**
  - Lists files changed in a specific commit.
  - `commit_hash`: The hash of the commit.
  - `cwd`: Working directory (optional).

- **`git_is_git_repo(cwd: Optional[str] = None)`**
  - Checks if a directory is a Git repository.
  - `cwd`: Directory to check (optional).

## Development

To set up the development environment:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```
