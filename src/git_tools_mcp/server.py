import subprocess
import argparse
from typing import List, Optional
import os
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("git-tools")

def run_git_command(command: List[str], cwd: Optional[str] = None, timeout: Optional[int] = None) -> str:
    """
    Run a git command and return its output.
    
    Args:
        command (List[str]): The git command and its arguments.
        cwd (Optional[str]): The working directory to run the command in.
        timeout (Optional[int]): Timeout for the command in seconds. 
    """
    try:
        result = subprocess.run(
            ["git"] + command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return (f"Git command failed: {e.stderr.strip()}")
    except subprocess.TimeoutExpired as e:
        return "Git command timed out"

@mcp.tool()
def git_get_commit_history(n: int = 10, cwd: Optional[str] = None) -> List[str]:
    """
    Get the last n commit hashes.

    Args:
        n (int): Number of commits to retrieve.
        cwd (Optional[str]): The working directory to run the command in.
    """
    output = run_git_command(["log", f"-n{n}", "--pretty=format:%H"], cwd=cwd)
    return output.splitlines()

@mcp.tool()
def git_get_commit_message(commit_hash: str, cwd: Optional[str] = None) -> str:
    """
    Get the commit message for a given commit hash.
    
    Args:
        commit_hash (str): The commit hash.
        cwd (Optional[str]): The working directory to run the command in. 
    """
    return run_git_command(["log", "-1", "--pretty=format:%B", commit_hash], cwd=cwd)

@mcp.tool()
def git_get_commit_diff(commit_hash: str, cwd: Optional[str] = None) -> str:
    """ Get the diff for a given commit hash.
    
    Args:
        commit_hash (str): The commit hash.
        cwd (Optional[str]): The working directory to run the command in. 
    """
    return run_git_command(["show", commit_hash, "--pretty=format:", "--unified=0"], cwd=cwd)

@mcp.tool()
def git_get_changed_files(commit_hash: str, cwd: Optional[str] = None) -> List[str]:
    """
    Get the list of files changed in a given commit.
    
    Args:
        commit_hash (str): The commit hash.
        cwd (Optional[str]): The working directory to run the command in. 
    """
    output = run_git_command(["diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash], cwd=cwd)
    return output.splitlines()

@mcp.tool()
def git_is_git_repo(cwd: Optional[str] = None) -> bool:
    """
    Check if the given directory is a git repository.

    Args:
        cwd (Optional[str]): The directory to check.  
    """
    try:
        run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
        return True
    except RuntimeError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Git Tools MCP Server")
    parser.add_argument("--http", action="store_true", help="Run as HTTP server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run HTTP server on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the HTTP server on (default: 127.0.0.1)")
    args, unknown = parser.parse_known_args()
    
    if args.http:
        mcp.settings.port = args.port
        mcp.settings.host = args.host
        mcp.run(transport="http")
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
