import sys
import settings
settings.init(sys.argv)

from tornado import web, ioloop, options
import handlers_svelte as svelte
import handlers_rtk as rtk

global application


if __name__ == "__main__":

    # clients = []
    handlers = [
        (r'/',                 svelte.RootHandler),
        (r'/services',         svelte.ServiceHandler),
        (r'/heartbeat',        svelte.HeartBeatHandler),
        (r'/status',           svelte.StatusHandler),
        (r'/job',              svelte.JobHandler),
        (r'/revoke',           svelte.RevokeHandler),
        (r'/dbcollections',    svelte.GetDBCollections),
        (r'/getdata',          svelte.GetMongoData),
        (r'/deletedata',       svelte.DropCollection),
        # (r'/response/ws',      rtk.EchoWebSocket, {'clients': clients}),
        (r'/response/ws',      rtk.EchoWebSocket),
        (r'/evaluate_rtk',     rtk.RTK_Evaluate),
        (r'/(.*)',             web.StaticFileHandler, {'path': svelte.GetStaticFolderPath()}),
    ]

    # Turn debug on to have Tornado restart when you change this file
    # Recommended when you're developing. Dont forget to remove it
    # when you put this in production
    #
    # app = tornado.web.Application(handlers, debug = True)
    #

    application = web.Application(handlers)

    io_loop = ioloop.IOLoop.instance()
    application.pc = rtk.PikaClient(io_loop)
    application.pc.connect()

    application.listen(options.options.port)

    print('Tornado has started at %s' % options.options.port, flush=True)
    ioloop.IOLoop.instance().start()
