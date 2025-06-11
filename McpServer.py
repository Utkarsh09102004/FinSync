from typing import Dict, Any, Optional, List
import asyncio
from mcp.server.fastmcp import FastMCP
import json

# Import your existing functions
from working_with_zoho_api.general_shit.trying_p_and_l import fetch_profit_and_loss

# Initialize FastMCP server
mcp = FastMCP("finsync-tools")

# ===== Financial Tools =====
@mcp.tool()
async def get_profit_and_loss(
    organization_id: Optional[str] = None,
    date_ranges: List[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieves profit and loss data from Zoho Books API for multiple date ranges.

    Args:
        organization_id: Zoho organization ID. If None, uses default from environment.
        date_ranges: A list of date ranges. Each range is a dictionary
                     with "from_date" and "to_date" keys in YYYY-MM-DD format.
                     Example: [{"from_date": "2024-04-01", "to_date": "2024-04-30"}]

    Returns:
        A list of structured profit and loss data for each date range.
    """
    if not date_ranges:
        return []

    loop = asyncio.get_event_loop()
    tasks = []
    for date_range in date_ranges:
        from_date = date_range.get("from_date")
        to_date = date_range.get("to_date")
        if from_date and to_date:
            task = loop.run_in_executor(
                None,  # Use default executor
                fetch_profit_and_loss,
                organization_id,
                from_date,
                to_date,
            )
            tasks.append(task)

    results = await asyncio.gather(*tasks)
    return list(results)

# ===== Easy to add more tools in categorized sections =====
@mcp.tool()
async def get_balance_sheet():
    """Documentation for balance sheet tool"""
    ...
    pass

@mcp.tool()
async def get_cash_flow():
    """Documentation for cash flow tool"""
    ...
    pass

# ===== Utility Tools =====
# @mcp.tool
# async def list_available_reports() -> Dict[str, str]:
#     """
#     Lists all available financial reports with descriptions.
    
#     Returns:
#         Dictionary mapping report names to their descriptions.
#     """
#     return {
#         "profit_and_loss": "Income statement showing revenue, expenses and resulting profit or loss",
#         # Add other reports as you implement them
#     }

# Main function to run the server


if __name__ == "__main__":
    print("Starting server...")
    mcp.run()
    print("Server started")