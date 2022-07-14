from tornado import web, ioloop, escape
from tornado_swagger.setup import setup_swagger
from bson.objectid import ObjectId
from pymongo import MongoClient
from gridfs import GridFS
import api_docs
import pymongo


######## MongoDB settings
client = MongoClient("mongodb", username="user", password="password", authSource="admin") # ssl=True ssl_certfile='/home/server/certs/cert.pem', ssl_keyfile='/home/server/certs/key.pem'
db = client["recovery_db"]
grid_fs = GridFS(db)
# CONST
MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB
MAX_STREAMED_SIZE = 16*GB


# cn=collection_name, document={"something_key": something_value, ...}
def insertData(cn, document, many=False):
    try:
        collection = db[cn]
        try:
            if many:
                return [str(i) for i in collection.insert_many(document).inserted_ids]
            else:
                _id = collection.insert(document)
                return str(_id)
        except:
            return None
    except:
        return None

# cn=collection_name, qo=query_object, po=projection_object
def getData(cn, qo={}, po=None):
    try:
        collection = db[cn]
        try:
            if po is None:
                return collection.find(qo)
            else:
                return collection.find(qo, po)
        except:
            return None
    except:
        return None

# cn=collection_name, arg=delete_document, del_many=boolean
def deleteData(cn, arg, many=False):
    try:
        collection = db[cn]
        try:
            if many:
                return collection.delete_many(arg) # arg = {"_id": {"$in": oid_list}}
            else:
                return collection.delete_one(arg)
        except:
            return None
    except:
        return None

# querz gridfs for files
def getFiles(file_id_string):
    return grid_fs.find_one({"_id": ObjectId(file_id_string)})
        
def insertFile(data, fname, content_type=None, encdng=None):
    if content_type is not None and encdng is not None:
        return grid_fs.put(data, filename=fname, contentType=content_type, encoding=encdng)
    else:
        return grid_fs.put(data, filename=fname)

def existFile(qo):
    return grid_fs.exists(qo)

def deleteFile(file_id_string):
    grid_fs.delete(ObjectId(file_id_string))


############ API Handler
class WelcomeHandler(web.RequestHandler):
    '''
    WelcomeHandler says hi.
    '''
    def get(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({"data": "Welcome to the Recovery Toolkit API :)."})


class StatusHandler(web.RequestHandler):
    '''
    ServiceHandler describes which services the response toolkit provides
    '''
    def get(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({
            "data": {
                "description": "The recovery toolkit provides the following services.",
                "services": [{"handle1": "upload checkpoint", "handle2": "upload logs"}]
            }
        })


class HeartBeatHandler(web.RequestHandler):
    '''
    HeartBeatHandler reacts on heartbeat requests.
    '''
    def get(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({"data": "Alive."})


class LogRollBack(web.RequestHandler):
    '''
    LogRollBack 
    '''
    def get(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({"data": "Alive."})

    def post(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({"data": "Alive."})


@web.stream_request_body
class UploadCheckpoint(web.RequestHandler):
    '''
    UploadCheckpoint uploads .tar file
    '''
    def initialize(self):
        self.bytes_read = 0
        self.data = b''

    def prepare(self):
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def data_received(self, chunck):
        self.bytes_read += len(chunck)
        self.data += chunck

    def post(self):
        '''
        HTTP GET Method handler
        '''
        this_request = self.request
        # value = self.data
        # with open('file', 'wb') as f:
        #     f.write(value)

        fs_id = insertFile(self.data, "test.tar", None, "application/octet-stream")
        respnse = {"gridfs_id": str(fs_id), "filename": "test.tar"}
        return self.finish(respnse)


# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Upload</title>
# </head>
# <body>
#     <h1>Upload</h1>
#     <form action="/upload" method="post" enctype="multipart/form-data">
#         <input type="file" name="file" id="file" />
#         <br />
#         <input type="submit" value="upload" />
#     </form>
# </body>
# </html>


class UploadLog(web.RequestHandler):
    '''
    UploadLog 
    '''
    def post(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({"data": "UploadLog called."})


class UploadLogFile(web.RequestHandler):
    '''
    UploadLogFile 
    '''
    def post(self):
        '''
        HTTP GET Method handler
        '''
        return self.finish({"data": "UploadLogFile called."})


class CheckpointRollBack(web.RequestHandler):
    '''
    CheckpointRollBack returns .tar file
    '''
    async def post(self):
        '''
        HTTP GET Method handler
        '''
        json_data = escape.json_decode(self.request.body)
        file_id = json_data["file_id"]
        file = getFiles(file_id)
        data = file.read()

        print(type(file), file, flush=True)

        # chunk_size = 256 * 1024
        # for i in range(0, len(data), chunk_size):
        #     self.write(bytes(data[i:i + chunk_size]))
        #     await self.flush()

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + "recovery-test.tar")

        self.write(data)
        self.finish()


class Application(web.Application):
    _routes = [
        web.url(r"/api/posts",          api_docs.PostsHandler),
        web.url(r"/api/posts/(\w+)",    api_docs.PostsDetailsHandler),
    ]

    def __init__(self, handlers):
        settings = {"debug": True} # remove it, when you put this in production

        for handler in handlers:
            self._routes.append(handler)

        # setup_swagger(handlers)
        setup_swagger(
            self._routes,
            swagger_url="/api",
            api_base_url="/",
            description="The toolkit allows to execute recovery strategies.",
            api_version="1.0.0",
            title="Recovery Toolkit API",
            contact="jan.lauinger@tum.de"
        )
        # super(Application, self).__init__(handlers)
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":

    handlers = [
        web.url(r'/',                       WelcomeHandler),
        web.url(r'/status',                 StatusHandler),
        web.url(r'/heartbeat',              HeartBeatHandler),

        web.url(r'/upload-checkpoint',      UploadCheckpoint),
        web.url(r'/upload-log',             UploadLog),
        web.url(r'/upload-logfile',         UploadLogFile),
        web.url(r'/checkpoint-rollback',    CheckpointRollBack),
        web.url(r'/log-rollback',           LogRollBack),
    ]

    application = Application(handlers)
    io_loop = ioloop.IOLoop.instance()
    application.listen(5000)

    ioloop.IOLoop.instance().start()

    print("The recovery Toolkit has started at 5000, with docs exposed at /api.", flush=True)
