# your_client_file.py

import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from working_with_zoho_api.auth.get_access_token import get_valid_access_token

ZOHO_ORGANIZATION_ID = "60040042565"

async def main():
    # Get a valid Zoho access token
    access_token = get_valid_access_token()
    if not access_token:
        print("Failed to get a valid Zoho access token. Exiting.")
        return

    # Configure the transport with the required headers
    transport = StreamableHttpTransport(
        url="http://127.0.0.1:8002/mcp",
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-Zoho-Organization-ID": ZOHO_ORGANIZATION_ID,
        },
    )

    # The client will use these headers for all subsequent calls
    async with Client(transport) as client:
        print("Calling tool with custom headers...")
        result = await client.call_tool(
            "get_profit_and_loss",
            {"date_ranges": [{"from_date": "2024-01-01", "to_date": "2024-01-31"}]}
        )
        print("Result:", result[0].text)

if __name__ == "__main__":
    asyncio.run(main())