from pymongo import MongoClient
from gridfs import GridFS
from tornado import options
import json
import pika
import time

def init(args):

    # sleep and wait for other services to boot up
    # required, otherwise connection to rabbitMQ fails
    time.sleep(17)

	# global variables
    global db, grid_fs, configs, connection, mgo_client # sec_channel

    # mongodb connection
    try:
        client = MongoClient("mongodb", username="user", password="password", authSource="admin") # ssl=True ssl_certfile='/home/server/certs/cert.pem', ssl_keyfile='/home/server/certs/key.pem'
        db = client["db"]
        grid_fs = GridFS(db)
    except:
        print("--MongoDB connection failed--")

    # read in config file
    with open("config.json") as f:
        configs = json.load(f)

    # tornado settings
    options.parse_command_line()
    options.define("port", default=configs["http_port"], help="Run on the given port", type=int)

    # init rabbit connection
    # credentials = pika.PlainCredentials('user', 'password')
    # parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    # connection = pika.BlockingConnection(parameters)
    # sec_channel = connection.channel()
    # sec_channel.queue_declare(queue='security_incident')

    # mongoDB connection
    mgo_client = MongoClient("mongodb", username="user", password="password", authSource="admin")
