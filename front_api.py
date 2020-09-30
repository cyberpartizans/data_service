import json
import argparse
from typing import Optional, Awaitable

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler, Application

from simple_settings import settings
from aiohttp import ClientSession

params_parser = argparse.ArgumentParser(description='Process some integers.')
params_parser.add_argument('--port')


class FaceHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        async with ClientSession() as session:
            face_results = await self.fetch(session=session, method='POST',
                                            url=settings.MODEL_SERVICE_ENDPOINT,
                                            headers=settings.FACE_SERVICE_HEADERS, data=data)

        self.write(face_results)
        await self.finish()

    @staticmethod
    async def fetch(session: ClientSession, url: str, method: str = 'POST', headers: dict = None, data: dict = None):
        async with session.request(method=method, url=url, headers=headers, data=data) as response:
            return await response.json()

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


class DataHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        async with ClientSession() as session:
            face_results = await self.fetch(session=session, method='POST',
                                            url=settings.MODEL_SERVICE_ENDPOINT,
                                            headers=settings.FACE_SERVICE_HEADERS, data=data)
        self.write(face_results)
        await self.finish()

    @staticmethod
    async def fetch(session: ClientSession, url: str, method: str = 'POST', headers: dict = None, data: dict = None):
        async with session.request(method=method, url=url, headers=headers, data=data) as response:
            return await response.json()

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


def create_app():
    app = Application([
        (r"/analyze_face", FaceHandler),
        (r"/add_data", DataHandler),
        (r"/add_unknown", DataHandler),
        (r"/update_unknown", DataHandler)
    ])

    return app


if __name__ == "__main__":
    args = params_parser.parse_args()

    port = int(args.port)
    server = HTTPServer(create_app())
    server.listen(port)
    server.start()  # Forks multiple sub-processes
    print('Server started at the %d port' % port)
    IOLoop.current().start()
