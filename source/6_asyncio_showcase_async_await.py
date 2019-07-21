import aiohttp
import asyncio
import time


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'http://localhost:8080')

start = time.time()

loop = asyncio.get_event_loop()
tasks = [loop.create_task(main()) for i in range(1000)]
wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)
loop.close()

print(f"It took {time.time() - start}")