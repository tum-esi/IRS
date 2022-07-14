import pika
import os, sys
import json

# main function for amqp publish subscribe testing
def main():

    # rabbitMQ connection:
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # create "hello" queue, otherwise rabbit drops messages if send to non-existing location
    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='security_incident')

    data = {
        "uiid":"793b8add-184d-489b-8f30-39527fe7f3b7",
        "type":"DDOS attack",
        "taxonomy":["infrastructure layer", "SYN flood", "TCP"],
        "timestamp_started":"2020-09-03 00:43:35.520",
        "timestamp_finished":"2020-09-03 03:17:21.116",
        "severity":"5",
        "sources":[
            "6.139.209.173",
            "43.118.93.222",
            "122.45.38.175"
        ],
        "targets":[{
            "uuid":"80e73532-52c2-4b57-affe-47afffc5e6b3",
            "ip":"172.17.0.5"
        }]
    }
    data2 = {"Hello": "World!"}

    # send binary data
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
    # to send JSON, use the following code:
    channel.basic_publish(exchange='',
        routing_key='security_incident',
        body=json.dumps(data2),
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ))
    channel.basic_publish(exchange='',
        routing_key='security_incident',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        ))
    
    print(" [x] Sent 'Hello World!'")
    print(" [x] Sent {'Hello': 'World!'}")
    print(" [x] Sent ", data)

    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

# sample code from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html
