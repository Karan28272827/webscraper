import asyncio
import json

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


async def extract_crypto_prices():
    # 1. Define a simple extraction schema
    schema = {
        "name": "Crypto Prices",
        "baseSelector": "div.crypto-row",  # Repeated elements
        "fields": [
            {"name": "coin_name", "selector": "h2.coin-name", "type": "text"},
            {"name": "price", "selector": "span.coin-price", "type": "text"},
        ],
    }

    # 2. Create the extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # 3. Set up your crawler config (if needed)
    config = CrawlerRunConfig(
        # e.g., pass js_code or wait_for if the page is dynamic
        # wait_for="css:.crypto-row:nth-child(20)"
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        # 4. Run the crawl and extraction
        result = await crawler.arun(
            url="https://www.trademap.org/Index.aspx",
            config=config,
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return

        # 5. Parse the extracted JSON
        data = json.loads(result.extracted_content)
        print(f"Extracted {len(data)} coin entries")
        print(json.dumps(data[0], indent=2) if data else "No data found")


asyncio.run(extract_crypto_prices())
