from tornado import concurrent, gen, ioloop
import settings
import events
import tasks
import json
import base64
import pika
import time
import datetime
from pika.adapters import tornado_connection


class PikaClient():
    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connected = False
        self.connection = None
        self.channel = None

        # celery_tasks stores all actively running celery tasks
        self.celery_tasks = []

    def connect(self):
        credentials = pika.PlainCredentials('user', 'password')
        param = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials, heartbeat=30) # blocked_connection_timeout=300
        self.connection = tornado_connection.TornadoConnection(param, custom_ioloop = self.io_loop, on_open_callback = self.on_connected)
        self.connection.add_on_open_error_callback(self.err)
        self.connection.add_on_close_callback(self.on_connection_closed)

    def err(self, conn):
        print('socket error', conn, flush=True)
        pass

    def on_connected(self, conn):
        print('connected', flush=True)
        self.connected = True
        self.connection = conn
        self.connection.channel(channel_number = 1, on_open_callback = self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        channel.queue_declare(queue='security_incident')
        channel.basic_consume(on_message_callback = self.on_message, queue='security_incident', auto_ack=True)
        return

    def on_connection_closed(self, conn, c):

        self.connection = None
        self.ioloop.call_later(5, self.connect)

    def add_celery_tasks(self, task):
        self.celery_tasks.append(task)

    def remove_celery_tasks(self, task):
        self.celery_tasks.remove(task)

    def get_celery_tasks(self):
        return self.celery_tasks

    def check_status(self, celery_task, future):
        if not celery_task.ready():
            ioloop.IOLoop.current().call_later(1, self.check_status, celery_task, future)
        else:
            future.set_result(celery_task.result)
            self.remove_celery_tasks(celery_task)
            # return future.result()

    @gen.coroutine
    def on_message(self, channel, method, properties, body):

        ################################### RABBIT CLIENT START PART
        print(body, flush=True)

        body = body.decode('utf8')
        data = json.loads(body)

        ################################### RESPONSE TOOLKIT PROTOCOL LOGIC START

        # log
        ts = time.time()
        print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], flush=True)
        
        print("data: ", data, data["uuid"], flush=True)
        # event to queue
        event = events.EVENT_RECEIVED
        event_not_exit = events.ERROR_NOT_EXIST

        print("event: ", event, flush=True)

        try:
            event["input_event"]["uuid"] = data["uuid"]
            event["input_event"]["type"] = data["type"]
            event_not_exit["input_event"]["uuid"] = data["uuid"]
            event_not_exit["input_event"]["type"] = data["type"]
        except:
            print("[error] accessing data event", flush=True)
            return

        push_notification(event)
        
        # preprocessing: event generation
        policy = ""
        ip = ""
        uuid = ""
        name = "response agent"
        payload = {}

        if data["type"] == "DDOS attack":
            policy = "block"
            # ip = data["targets"][0]["uuid"]
            ip = "172.18.0.9"
            uuid = data["targets"][0]["ip"]

        elif data["type"] == "local DDOS attack":
            policy = "block"
            uuid = data["targets"][0]["uuid"]
            # ip = "172.18.0.9"
            ip = "response-agent"
            payload["local"] = True

        elif data["type"] == "Notification":
            policy = "passive response, notification"
            event["response"] = "test notification works for timing check"
            push_notification(event)
            return
        else:
            push_notification(event_not_exit)

        print("ip request:", ip, data["type"], flush=True)

        # build response
        payload["policy"] = policy
        payload["ip"] = ip

        # set events, immediate access works, because checked with try except above
        err_internal = events.ERROR_INTERNAL
        err_internal["input_event"] = {
            "uuid": data["uuid"],
            "type": data["type"]
        }
        event = events.EVENT_COMPLETED
        event["input_event"] = {
            "uuid": data["uuid"],
            "type": data["type"]
        }

        ################################### RESPONSE TOOLKIT PROTOCOL LOGIC END

        ################################### RESPONSE CELERY PROCESS START

        future = concurrent.Future()
        celery_task = tasks.automated_task.delay(payload)
        # celery_task = tasks.add.delay(3, 5)
        self.add_celery_tasks(celery_task)
        self.check_status(celery_task, future)
        yield future
        result = future.result()

        ################################### RESPONSE CELERY PROCESS START

        ################################### RABBIT CLIENT END PART

        event["result"] = result # json.dumps(result)
        push_notification(event)
        pass


def push_notification(data):
    
    # check if channel still open
    if not settings.note_channel or settings.note_channel.is_closed:
        settings.note_channel = settings.pikaReconnect()

    # event timestamp
    ts = time.time()
    data["epoche"] = ts
    data["date"] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # publish message
    settings.note_channel.basic_publish(exchange='',
        routing_key='notification',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        )
    )

    # log
    ts = time.time()
    print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], flush=True)
    return
