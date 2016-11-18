import tornado.ioloop
import tornado.web

from main import get_crawled_result

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        url = self.get_argument('url')
        res = get_crawled_result(url)
        self.write(res)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()