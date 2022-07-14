from tornado import web, escape, gen, httpclient
from os import path
import mymongo
import datetime
import requests
import json
import asyncio
import settings

# staticFolder ="svelte-frontend/public/"
staticFolder ="frontend/build/"
svelteAppPath = path.abspath(path.dirname(__file__))+'/'+staticFolder


def GetStaticFolderPath():
    return staticFolder


class RootHandler(web.RequestHandler):
    '''
    Handler to serve the template/index.html
    '''
    def get(self):
        '''
        HTTP GET Method handler
        '''
        with open(svelteAppPath + "index.html", 'r') as file:
            self.write(file.read())


class StatusHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):

        ts_start = datetime.datetime.now()
        http_client = httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://response-toolkit:5000/status")
        json_data = json.loads(response.body)

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": json_data, "request_duration_ms": execution_time})


class ServiceHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):

        ts_start = datetime.datetime.now()
        http_client = httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://response-toolkit:5000/services")
        json_data = json.loads(response.body)

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": json_data, "request_duration_ms": execution_time})


class HeartBeatHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):

        ts_start = datetime.datetime.now()
        http_client = httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://response-toolkit:5000/heartbeat")
        json_data = json.loads(response.body)

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": json_data, "request_duration_ms": execution_time})


class JobHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):

        # body = escape.json_decode(self.request.body)
        ts_start = datetime.datetime.now()
        client = httpclient.AsyncHTTPClient()
        headers = {"Content-Type": "application/json"}
        response = yield client.fetch(
            "http://response-toolkit:5000/job",
            method="POST",
            headers=headers,
            # allow_nonstandard_methods=True,
            body=self.request.body,
        )
        json_data = json.loads(response.body)

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": json_data, "request_duration_ms": execution_time})


class RevokeHandler(web.RequestHandler):

    @gen.coroutine
    def post(self):

        # payload = escape.json_decode(self.request.body)
        ts_start = datetime.datetime.now()
        client = httpclient.AsyncHTTPClient()
        headers = {"Content-Type": "application/json"}
        response = yield client.fetch(
            "http://response-toolkit:5000/revoke",
            method="POST",
            headers=headers,
            body=self.request.body,
        )
        json_data = json.loads(response.body)

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": json_data, "request_duration_ms": execution_time})


class GetDBCollections(web.RequestHandler):

    @gen.coroutine
    def get(self):

        ts_start = datetime.datetime.now()        
        d = dict((db, [collection for collection in settings.mgo_client[db].list_collection_names()])
                for db in settings.mgo_client.list_database_names())

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": json.dumps(d), "request_duration_ms": execution_time})


class GetMongoData(web.RequestHandler):

    @gen.coroutine
    def post(self):

        ts_start = datetime.datetime.now()

        # print("data:", self.request.body, flush=True)
        
        body = escape.json_decode(self.request.body)
        data = [i for i in mymongo.getData(body["db_name"], body["collection_name"])]

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        return self.finish({"return_data": data, "request_duration_ms": execution_time})


class DropCollection(web.RequestHandler):

    @gen.coroutine
    def post(self):

        ts_start = datetime.datetime.now()
        body = escape.json_decode(self.request.body)
        data = mymongo.deleteData(body["db_name"], body["collection_name"], {}, True)

        ts_end = datetime.datetime.now()
        time_diff = (ts_end - ts_start)
        execution_time = time_diff.total_seconds() * 1000

        if data != None:
            return self.finish({"return_data": {"status": "delete success"}, "request_duration_ms": execution_time})
        else:
            return self.finish({"return_data": {"status": "delete failure"}, "request_duration_ms": execution_time})
