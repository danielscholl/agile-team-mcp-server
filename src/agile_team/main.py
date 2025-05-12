"""Entry point for the Agile Team MCP Server."""

import sys
import argparse
from agile_team.server import mcp
from agile_team import __version__


def main():
    """Run the Agile Team MCP server."""
    parser = argparse.ArgumentParser(description="Agile Team MCP Server")
    parser.add_argument(
        "--version", 
        action="store_true", 
        help="Show version information and exit"
    )
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Agile Team MCP Server v{__version__}")
        sys.exit(0)
    
    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()