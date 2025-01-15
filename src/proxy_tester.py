import aiohttp
import asyncio
import logging

async def test_proxy(session, proxy):
    proxy_url = proxy.split('//')[-1] if '://' in proxy else proxy
    try:
        async with session.get('https://httpbin.org/get', proxy=proxy, timeout=2) as response:
            if response.status == 200:
                logging.info(f"Proxy {proxy_url} is working.")
                return proxy_url
    except Exception as e:
        logging.error(f"Proxy {proxy_url} failed: {e}")

async def test_proxies(proxies):
    async with aiohttp.ClientSession() as session:
        tasks = [test_proxy(session, proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        working_proxies = [proxy for proxy in results if isinstance(proxy, str)]
        return working_proxies
