import tornado.ioloop
import tornado.web
import logging
from util import WebLogger

from handlers.logger import EventHandler


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'default_handler_args': dict(status_code=404),
        }

        app_handlers = [
            (r'^/$', EventHandler),
        ]

        self.event_logger = WebLogger(s3_bucket='aws-website-adamkelleher-q9wlb',
                                      s3_path='pageviews',
                                      log_file_path='/app/tmp')
        super(Application, self).__init__(app_handlers, **app_settings)


if __name__ == "__main__":
    port = 8889
    address = '0.0.0.0'
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting event logger on %s:%d', address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True)
    http_server.listen(port, address=address)

    tornado.ioloop.IOLoop.instance().start()
