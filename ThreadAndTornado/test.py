import platform
import time

import tornado.web
import tornado.httpserver
from tornado import gen, ioloop
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.options import options, define


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class IndexHandler(BaseHandler):
    def get(self):
        self.write('index')


class NonBlockingHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self):
        result = yield self.doing()
        self.write(result)

    @run_on_executor
    def doing(self):
        time.sleep(10)
        return 'Non-Blocking'


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/index", IndexHandler),
        (r"/nonblocking", NonBlockingHandler),
    ])
    define('p', default=8000, type=int, help='listen port')
    define('h', default='0.0.0.0', type=str, help='listen address')
    options.parse_command_line()
    application.listen(port=options.p, address=options.h)
    server = tornado.httpserver.HTTPServer(application)
    if platform.system() == 'linux':
        server.start(None)
    else:
        server.start(1)
        # pass
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.instance().stop()
