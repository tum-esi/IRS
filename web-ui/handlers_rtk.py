from tornado import web, escape, websocket, gen
import settings
from tornado.iostream import StreamClosedError
import asyncio
import json
import pika
from pika.adapters import tornado_connection

# basis code from
# https://reminiscential.wordpress.com/2012/04/07/realtime-notification-delivery-using-rabbitmq-tornado-and-websocket/


class PikaClient():
    def __init__(self, io_loop):
        
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.ws_clients = []

    def add_ws_clients(self, client):
        self.ws_clients.append(client)

    def remove_ws_clients(self, client):
        self.ws_clients.remove(client)

    def connect(self):
        if self.connecting:
            return
        self.connecting = True
        credentials = pika.PlainCredentials('user', 'password')
        param = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
        self.connection = tornado_connection.TornadoConnection(param, custom_ioloop = self.io_loop, on_open_callback = self.on_connected)
        self.connection.add_on_open_error_callback(self.err)
        self.connection.add_on_close_callback(self.on_closed)

    def err(self, conn):
        print('socket error', conn, flush=True)
        pass

    def on_connected(self, conn):
        print('connected', flush=True)
        self.connected = True
        self.connection = conn
        self.connection.channel(channel_number = 1, on_open_callback = self.on_channel_open)

    def on_message(self, channel, method, properties, body):
        print(body, flush=True)

        for client in self.ws_clients:
            client.write_message(body)
        pass

    def on_channel_open(self, channel):
        self.channel = channel
        channel.queue_declare(queue='notification')
        channel.basic_consume(on_message_callback = self.on_message, queue='notification', auto_ack=True)
        return

    def on_closed(self, conn, c):
        print('pika close!', flush=True)
        self.io_loop.stop()
        pass


class EchoWebSocket(websocket.WebSocketHandler):

    def open(self):
        self.application.pc.add_ws_clients(self)

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        self.application.pc.remove_ws_clients(self)


class RTK_Evaluate(web.RequestHandler):

    # @gen.coroutine
    def post(self):

        credentials = pika.PlainCredentials('user', 'password')
        parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        sec_channel = connection.channel()
        # sec_channel.queue_declare(queue='security_incident')

        # pre-process data and fill q
        data = json.loads(self.request.body.decode('utf-8'))

        # send security incidents
        for x in range(0, int(data["incident_number"])):

            sec_channel.basic_publish(exchange='',
                routing_key='security_incident',
                body=json.dumps(data["incident_data"]),
                properties=pika.BasicProperties(
                    delivery_mode = 2, # make message persistent
                ))

        sec_channel.close()

        return self.finish({"data": "Published all {} messages".format(data["incident_number"])})
