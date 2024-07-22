"""
Tornado Web Server for Full Django App
Please place this file in the same folder with the django project root directory
"""

import functools
import os
import signal
import time

import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
from tornado.options import define, options

try:
    define("port", default=8888, help="run on the given port", type=int)
except:
    pass

try:
    define(
        "log_file_prefix",
        type=str,
        default=None,
        metavar="PATH",
        help=(
            "Path prefix for log files. "
            "Note that if you are running multiple tornado processes, "
            "log_file_prefix must be different for each of them (e.g. "
            "include the port number)"
        ),
    )
except:
    pass


def stop_server(server, loop):
    server.stop()
    loop.add_timeout(time.time() + 5.0, functools.partial(stop_loop, loop))


def stop_loop(loop):
    loop.stop()


def sighup_handler(http_server, ioloop, signum, frame):
    ioloop.add_callback(functools.partial(stop_server, http_server, ioloop))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings.dev"
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()
    application = django.core.handlers.wsgi.WSGIHandler()
    container = tornado.wsgi.WSGIContainer(application)

    http_server = tornado.httpserver.HTTPServer(container, xheaders=True)
    ioloop = tornado.ioloop.IOLoop.instance()

    signal.signal(
        signal.SIGHUP,
        lambda signum, frame: sighup_handler(http_server, ioloop, signum, frame),
    )

    port = options.port
    print("port", port)
    http_server.listen(port)
    ioloop.start()
