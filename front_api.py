import json
import argparse
from abc import ABC
from typing import Optional, Awaitable

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler, Application

from aiohttp import ClientSession

from read_settings import read_settings

params_parser = argparse.ArgumentParser(description='Process some integers.')
params_parser.add_argument('--port')

model_service_url, face_service_headers, tg_bot_headers, db_url, db_headers = read_settings


class BaseHandler(RequestHandler, ABC):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    @staticmethod
    async def fetch(session: ClientSession, url: str, method: str = 'POST', headers: dict = None, data: dict = None):
        async with session.request(method=method, url=url, headers=headers, data=data) as response:
            return await response.json()


class FaceHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        async with ClientSession() as session:
            face_results = await self.fetch(session=session, method='POST',
                                            url=model_service_url,
                                            headers=face_service_headers, data=data)

        self.write(face_results)
        await self.finish()

    @staticmethod
    async def fetch(session: ClientSession, url: str, method: str = 'POST', headers: dict = None, data: dict = None):
        async with session.request(method=method, url=url, headers=headers, data=data) as response:
            return await response.json()

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


class DataHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def post(self, *args, **kwargs):
        pass

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


def create_app():
    app = Application([
        (r"/analyze_face", FaceHandler),
        (r"/add_data", DataHandler),
        (r"/get_info", DataHandler),
        (r"/check_entity", DataHandler),
        (r"/update_data", DataHandler)
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
