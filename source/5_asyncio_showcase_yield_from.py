import aiohttp
import asyncio


@asyncio.coroutine
def fetch(session, url):
    response = yield from session.get(url)
    result = yield from response.text()
    return result


@asyncio.coroutine
def main():
    session = aiohttp.ClientSession()
    response = yield from fetch(session, 'http://localhost:8080')
    print(response)
    yield from session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())