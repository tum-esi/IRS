import pika
import sys, os
import json
import time
import requests
import datetime
import response_requests
import events

# example printing time in ms
def time_ms():
    start_time = datetime.datetime.now()
    time.sleep(2.4)
    elapsed = datetime.datetime.now() - start_time
    print(int(elapsed.total_seconds()*1000), flush=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def notificationChannel(ch, method, properties, body):
    print(" [x] Notification Received JSON %r" % json.loads(body))

def callbackJSON(ch, method, properties, body):

    # parse/de-serialize
    data = json.loads(body)

    # log
    ts = time.time()
    print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), flush=True)
    
    print("data: ", data, flush=True)
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

    push_event(ch, event, "notification")
    
    # processing
    policy = ""
    ip = ""
    uuid = ""
    name = "response agent"

    if data["type"] == "DDOS attack":
        policy = "block"
        # ip = data["targets"][0]["uuid"]
        ip = "172.18.0.9"
        uuid = data["targets"][0]["ip"]
    else:
        push_event(ch, event_not_exit, "notification")

    # build response
    payload = {
        "policy": policy,
        "ip": ip
    }

    # set events, immediate access works, because checked with try except above
    err_internal = events.ERROR_INTERNAL
    err_internal["input_event"] = {
        "uuid": data["uuid"],
        "type": data["type"]
    }
    event_intermediate = events.EVENT_INTERMEDIATE
    event_intermediate["input_event"] = {
        "uuid": data["uuid"],
        "type": data["type"]
    }
    event = events.EVENT_COMPLETED
    event["input_event"] = {
        "uuid": data["uuid"],
        "type": data["type"]
    }

    try:

        # logs
        ts = time.time()
        print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), flush=True)
        event_intermediate["status"] = "[sending] request to agent"
        push_event(ch, event_intermediate, "notification")
        
        r = agent_requests.certh(payload)
        if r.status_code == requests.codes.ok:

            ts = time.time()
            print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), flush=True)
            event_intermediate["status"] = "[received] request from agent"
            push_event(ch, event_intermediate, "notification")

            json_data = json.loads(r.text)
            push_event(ch, event, "notification")
        else:
            err_internal["status"] = "[internal error] response status code not 200"
            push_event(ch, err_internal, "notification", "status code not 200")

    except (requests.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e :
        push_event(ch, err_internal, "notification")
        

def push_event(ch, data, rk):
    
    # event timestamp
    ts = time.time()
    data["epoche"] = ts
    data["date"] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    # publish message
    ch.basic_publish(exchange='',
        routing_key=rk,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        )
    )

    # log
    ts = time.time()
    print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), flush=True)
    return

# main function for amqp publish subscribe testing
def main():

    # wait until rabbitMQ ready
    print("[sleep]", flush=True)
    time.sleep(15)
    print("[wake-up]", flush=True)

    # rabbitMQ connection:
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # if no credentials in use: 
    #   connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    #   channel = connection.channel()

    # create "hello" queue, otherwise rabbit drops messages if send to non-existing location
    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='security_incident')
    # for sending notifications
    channel.queue_declare(queue='notification')

    # connection of queue and message callback 
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)
    channel.basic_consume(queue='security_incident', auto_ack=True, on_message_callback=callbackJSON)
    # channel.basic_consume(queue='notification', auto_ack=True, on_message_callback=notificationChannel)

    print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
    channel.start_consuming()


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
