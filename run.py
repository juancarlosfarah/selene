# -*- coding: utf-8 *-*
import os
import pymongo
import tornado.web
import tornado.httpserver

from selene import options, handlers, modules, routes
from tornado.options import options as opts


class Selene(tornado.web.Application):

    def __init__(self, db):
        self.db = db
        self.path = os.path.dirname(__file__)
        settings = {
            'login_url': '/login',
            'static_path': os.path.join(self.path, '/'.join([opts.theme_path,
                'static'])),
            'template_path': os.path.join(self.path, '/'.join([opts.theme_path,
                'templates'])),
            'xsrf_cookies': True,
            'cookie_secret': opts.cookie_secret,
            'ui_modules': modules
        }
        tornado.web.Application.__init__(self, routes.urls +
            [(r"/(favicon\.ico)", tornado.web.StaticFileHandler,
            {'path': settings['static_path']})], **settings)

if __name__ == '__main__':
    options.setup_options('selene.conf')
    db = pymongo.MongoClient(opts.db_uri)[opts.db_name]
    tornado.locale.load_translations("translations")
    tornado.web.ErrorHandler = handlers.ErrorHandler
    http_server = tornado.httpserver.HTTPServer(Selene(db))
    http_server.listen(opts.port)
    tornado.ioloop.IOLoop.instance().start()