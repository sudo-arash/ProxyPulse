# Proxy Testing Logic

The proxy testing functionality is implemented in `src/proxy_tester.py` using `aiohttp` for asynchronous HTTP requests.

## Key Functions

- **`test_proxy(session, proxy)`**: Tests a single proxy by making a GET request to `https://httpbin.org/get`.
- **`test_proxies(proxies)`**: Tests a list of proxies concurrently using `asyncio.gather`.

## Workflow

1. The `test_proxy` function checks if a proxy is working by attempting to connect to a target URL.
2. If the proxy is functional, it is added to the list of working proxies.
3. The results are returned to the GUI for display.
