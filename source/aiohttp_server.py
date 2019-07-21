from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
app.add_routes([web.get('/', hello), web.get('/1', hello), web.get('/2', hello)])

web.run_app(app)
