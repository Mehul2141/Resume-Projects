import asyncio
import httpx
import time

URL = "http://localhost:8000/test"  # change if needed
TOTAL_REQUESTS = 500
CONCURRENCY = 20

async def fetch(client, i):
    try:
        response = await client.get(URL)
        print(f"[{i}] Status: {response.status_code}")
    except Exception as e:
        print(f"[{i}] Error: {e}")

async def run_load_test():
    async with httpx.AsyncClient(timeout=10.0) as client:
        start = time.time()
        await asyncio.gather(*(fetch(client, i) for i in range(TOTAL_REQUESTS)))
        duration = time.time() - start
        print(f"\n✅ Completed {TOTAL_REQUESTS} requests in {duration:.2f} seconds")
if __name__ == "__main__":
    asyncio.run(run_load_test())
