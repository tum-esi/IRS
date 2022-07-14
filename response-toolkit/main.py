import sys
import settings
settings.init(sys.argv)

from tornado import web, ioloop
from tornado_swagger.setup import setup_swagger
import tasks
import rabbit_client
import api_docs


class WelcomeHandler(web.RequestHandler):
    def get(self):
        return self.finish({"data": "Welcome to the Response Toolkit API :)."})


class ServiceHandler(web.RequestHandler):
    def get(self):
        return self.finish({
            "data": {
                "description": "The response toolkit provides the following services.",
                "services": [{"handle": "DDOS attack", "action": "IP address blocking"}]
            }
        })


class HeartBeatHandler(web.RequestHandler):
    def get(self):
        return self.finish({"data": "Alive."})


class Application(web.Application):
    _routes = [
        web.url(r"/api/heartbeat",    api_docs.HeartBeatHandler),
        web.url(r"/api/services",     api_docs.ServiceHandler),
        web.url(r"/api/revoke",       api_docs.RevokeJobHandler),
        web.url(r"/api/job/(\w+)",    api_docs.CeleryTasks),
    ]

    def __init__(self, handlers):
        settings = {"debug": True} # remove it, when you put this in production

        for handler in handlers:
            self._routes.append(handler)

        # setup_swagger(handlers)
        setup_swagger(
            self._routes,
            swagger_url="/doc",
            api_base_url="/",
            description="The toolkit allows to execute manual (via API) response strategies (celery jobs) asynchronously and automatically reacts to message broker (RabbitMQ) events.",
            api_version="1.0.0",
            title="Response Toolkit API",
            contact="jan.lauinger@tum.de"
        )
        # super(Application, self).__init__(handlers)
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":

    handlers = [
        web.url(r'/',               WelcomeHandler),
        web.url(r'/services',       ServiceHandler),
        web.url(r'/heartbeat',      HeartBeatHandler),

        web.url(r'/job',            tasks.CeleryTasks),
        web.url(r'/status',         tasks.StatusHandler),
        web.url(r'/revoke',         tasks.RevokeJobHandler),
    ]

    application = Application(handlers)
    io_loop = ioloop.IOLoop.instance()
    application.pc = rabbit_client.PikaClient(io_loop)

    application.pc.connect()
    application.listen(settings.configs["http_port"])

    ioloop.IOLoop.instance().start()
    # scheduler = ioloop.PeriodicCallback(application.pc.connect(), 20000)
    # scheduler.start()

    print("Tornado has started at 5000, with docs exposed at /doc.", flush=True)
