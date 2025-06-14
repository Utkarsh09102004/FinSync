# Install with pip install firecrawl-py
import asyncio
from firecrawl import AsyncFirecrawlApp
from firecrawl import ScrapeOptions

async def main():
    print("Starting...")
    app = AsyncFirecrawlApp(api_key='fc-f27f1a5d34064b4e8025c9f5eab7f075')
    response = await app.crawl_url(
        url='https://google.github.io/adk-docs/',
    	scrape_options = ScrapeOptions(
            limit= 100,
            formats= [ 'markdown' ],
            onlyMainContent= True
    	)
    )
    print(response)


asyncio.run(main())