import time
from concurrent.futures import ThreadPoolExecutor

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.concurrent import run_on_executor

# django settings must be called before importing models
from utils import init_django

init_django()

from db._models import Schema


class OriginalAsyncHandler(tornado.web.RequestHandler):
    """Make the task non-blocking use python's(>=3.7) async and await"""

    class Obj:

        def __init__(self, pk, name, desc):
            self.pk = pk
            self.name = name
            self.desc = desc

    async def get(self):
        print(1)
        # await asyncio.sleep(0.99)
        # time.sleep(5)
        print(2)
        # self.write("hello")
        res = [self.Obj(i, "a", "b") for i in range(10)]
        print(res)
        self.render(
            "templates/index.html",
            items=res,
        )


class BlockingToAsyncHandler(tornado.web.RequestHandler):
    """Make the task non-blocking, Supports the use of other libraries in code that do not support synchronization.

    **Asynchronous Programming Based on Thread Pool**

    If the other libraries being used, such as `time` and `urllib`, do not support asynchronous operations, the response will still be blocking.

    In Tornado, there is a decorator that can use `ThreadPoolExecutor` to turn blocking processes into non-blocking ones. The principle is to start a separate thread outside of Tornado's own thread to execute the blocking program, thereby making Tornado non-blocking.
    """

    # Must define an executor thread pool for decorator run_on_executor to work
    executor = ThreadPoolExecutor(max_workers=10)

    # Use @run_on_executor to make the task non-blocking, but need to create an executor first
    @run_on_executor
    def task(self):
        time.sleep(1)
        # url = "https://www.google.com/"
        # url = "https://www.baidu.com/"
        # import urllib.request

        # res = urllib.request.urlopen(url).read()
        # self.write('res')
        res = Schema.objects.all()
        return res

    # Use @tornado.gen.coroutine
    @tornado.gen.coroutine
    def get(self):
        print("-> get enter")
        # 2. use yield
        res = yield self.task()
        print("<- get outer", res)
        # self.write(res)
        self.render(
            "templates/index.html",
            items=res,
        )


# map the Urls to the class
application = tornado.web.Application(
    [
        (r"/", BlockingToAsyncHandler),
    ]
)


# Start the server
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
