# your_server_file.py

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request
from typing import Dict, Any, Optional, List
import asyncio

# Your other imports...
from working_with_zoho_api.general_shit.trying_p_and_l import fetch_profit_and_loss

mcp = FastMCP("finsync-tools")

# --- Helper function to make this logic reusable ---
def get_zoho_credentials() -> tuple[str, str]:
    """
    Extracts Zoho credentials from the current HTTP request headers.
    This is a reusable helper to avoid repeating logic in every tool.
    """
    try:
        request: Request = get_http_request()
    except RuntimeError:
        # This will happen if the tool is called outside an HTTP request context
        raise ToolError("This tool can only be used via an HTTP server.")

    # 1. Get the Access Token from the 'Authorization' header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise ToolError("Authorization header with Bearer token is missing or invalid.")
    access_token = auth_header.split("Bearer ")[1]

    # 2. Get the Organization ID from a custom header (e.g., 'X-Zoho-Organization-ID')
    organization_id = request.headers.get("X-Zoho-Organization-ID")
    if not organization_id:
        raise ToolError("X-Zoho-Organization-ID header is missing.")

    return access_token, organization_id


@mcp.tool
async def get_profit_and_loss(
    date_ranges: List[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieves profit and loss data from Zoho Books API for multiple date ranges.
    Requires Bearer token and organization ID in headers.
    """
    if not date_ranges:
        return []

    # Get credentials for this specific request
    access_token, organization_id = get_zoho_credentials()

    tasks = []
    for date_range in date_ranges:
        from_date, to_date = date_range.get("from_date"), date_range.get("to_date")
        if from_date and to_date:
            # Pass the retrieved credentials to your API-calling function
            task = asyncio.to_thread(
                fetch_profit_and_loss,
                organization_id,
                from_date,
                to_date,
                # You'll likely need to modify fetch_profit_and_loss to accept the token
                # access_token=access_token 
            )
            tasks.append(task)
    
    if not tasks:
        return []

    all_results = await asyncio.gather(*tasks)
    return all_results

# ... your other tools would also call get_zoho_credentials()

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)