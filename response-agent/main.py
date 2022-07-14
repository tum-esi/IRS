import tornado.ioloop
import tornado.web
import json

class ResponseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        return self.finish({"received": data, "result": "applied"})

def make_app():
    return tornado.web.Application([
        (r"/response", ResponseHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
