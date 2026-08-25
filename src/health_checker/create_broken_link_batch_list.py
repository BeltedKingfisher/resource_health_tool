import asyncio
import aiohttp
import socket

CONCURRENCY_LIMIT = 20
REQUEST_TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HealthChecker/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

async def check_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                allow_redirects=True
            ) as response:
                return {
                    "url": url,
                    "broken": response.status >= 400,
                    "status": response.status,
                    "error": None
                }
        except (aiohttp.ClientError, socket.gaierror) as e:
            return {
                "url": url,
                "broken": True,
                "status": None,
                "error": str(e)
            }
        except asyncio.TimeoutError:
            return {
                "url": url,
                "broken": True,
                "status": None,
                "error": "request timed out"
            }

async def check_batch_urls(urls: list[str]) -> dict:
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [check_url(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

    return {
        result["url"]: {"status": result["status"], "error": result["error"]}
        for result in results
        if result["broken"]
    }