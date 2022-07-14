from tornado import options, ioloop
import json
import pika
import time

def init(args):

    # wait until rabbitMQ is up
    time.sleep(18)

	# global variables
    global configs, connection, note_channel, pikaHeartbeat

    # read in config file
    with open("tornadoconfig.json") as f:
        configs = json.load(f)

    # tornado settings
    options.parse_command_line()

    # pika setting
    note_channel = pikaReconnect()

def pikaReconnect():
    try:
        credentials = pika.PlainCredentials('user', 'password')
        parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        note_channel = connection.channel()
        note_channel.queue_declare(queue='notification')
        return note_channel
    except:
        print("--RabbitMQ connection failed--")
        return None