import json
import time
import pika
import requests
import datetime
import response_requests
from celery import Celery
from celery.schedules import crontab
from tornado import web, concurrent, gen, ioloop, escape


celery = Celery('tasks', broker='amqp://user:password@rabbitmq:5672/jobs', backend='mongodb://mongodb:27017/jobs')
celery.conf.update(
    result_serializer='json',
    task_serializer='json',
    result_backend='mongodb',
    mongodb_backend_settings={
        "host": "mongodb", # docker specific
        "port": 27017,
        "username": "user",
        "password": "password",
        "database": "jobs",
        "taskmeta_collection": "stock_taskmeta_collection",
    },
    accept_content=['json'],
    broker_url='amqp://user:password@rabbitmq:5672/'
)

# regular tasks
@celery.task
def manual_task():
    # time.sleep(15)
    ts_start = time.time()
    ts_end = time.time()
    json_data = {}
    error_desc1 = None
    error_desc2 = None
    payload = {
        "policy": "block",
        "ip": "172.18.0.9"
    }
    try:
        r = response_requests.certh(payload)
        if r.status_code == requests.codes.ok:
            ts_end = time.time()
            json_data = json.loads(r.text)
        else:
            ts_end = time.time()
            error_desc2 = "[internal error] response status code not 200."

    except (requests.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e :
        error_desc1 = "[internal error] response-agent request failed."
        ts_end = time.time()

    return {
        "service": "block IP address",
        "actions": [
            {
                "name": "[request send] HTTP request to response-agent.",
                "start_time_stamp": datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                "start_epoch": ts_start,
            },
            {
                "name": "[request received] HTTP response from response-agent.",
                "end_time_stamp": datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                "end_epoch": ts_end
            }
        ],
        # None stands for no error occurred
        "errors": ["error_desc1", "error_desc2"],
        "data": {
            "response": json_data
        }
    }

@celery.task
def manual_task2():
    # time.sleep(15)
    ts_start = time.time()
    ts_end = time.time()
    error_desc1 = None
    error_desc2 = None
    payload = {
        "policy": "block",
        "ip": "response-agent"
    }
    try:
        r = response_requests.local_agent(payload)
        if r.status_code == requests.codes.ok:
            ts_end = time.time()
            json_data = json.loads(r.text)
        else:
            ts_end = time.time()
            error_desc2 = "[internal error] response status code not 200."

    except (requests.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e :
        error_desc1 = "[internal error] response-agent request failed."
        ts_end = time.time()

    ts_end = time.time()
    return {
        "service": "block IP address",
        "actions": [
            {
                "name": "[request send] HTTP request to response-agent.",
                "start_time_stamp": datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                "start_epoch": ts_start,
            },
            {
                "name": "[request received] HTTP response from response-agent.",
                "end_time_stamp": datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                "end_epoch": ts_end
            }
        ],
        # None stands for no error occurred
        "errors": ["error_desc1", "error_desc2"],
        "data": {
            "response": json_data
        }
    }

@celery.task
def add(x, y):
    time.sleep(15)
    ts = time.time()
    print("[celery add function] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], flush=True)
    return {"result": x + y}

@celery.task
def notify():
    
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    note_channel = connection.channel()
    note_channel.queue_declare(queue='notification')

    ts = time.time()
    date_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    data = {"title": "test manual notification message over broker", "date time": date_time}

    note_channel.basic_publish(exchange='',
        routing_key='notification',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode = 2, # make message persistent
        )
    )

    return {"result": "notification send to message broker"}

@celery.task
def automated_task(payload):

    print("in automated task:", payload, flush=True)
    ts_start = time.time()
    ts_end = time.time()
    json_data = {"msg": "no request send from response toolkit to any target"}
    error_desc1 = None
    error_desc2 = None
    try:
        if "local" in payload:
            r = response_requests.local_agent(payload)
            if r.status_code == requests.codes.ok:
                ts_end = time.time()
                json_data = json.loads(r.text)
            else:
                ts_end = time.time()
                error_desc2 = "[internal error] response status code not 200."
        else:
            r = response_requests.certh(payload)
            if r.status_code == requests.codes.ok:
                ts_end = time.time()
                json_data = json.loads(r.text)
            else:
                ts_end = time.time()
                error_desc2 = "[internal error] response status code not 200."

    except (requests.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e :
        error_desc1 = "[internal error] response-agent request failed."

    ts_end = time.time()
    return {
        "service": "block IP address",
        "actions": [
            {
                "name": "[request send] HTTP request to response-agent.",
                "start_time_stamp": datetime.datetime.fromtimestamp(ts_start).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                "start_epoch": ts_start,
            },
            {
                "name": "[request received] HTTP response from response-agent.",
                "end_time_stamp": datetime.datetime.fromtimestamp(ts_end).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
                "end_epoch": ts_end
            }
        ],
        # None stands for no error occurred
        "errors": [error_desc1, error_desc2],
        "data": {
            "response": json_data
        }
    }


########## tornado handler

class StatusHandler(web.RequestHandler):
    '''
    StatusHandler checks if jobs are running
    '''
    def get(self):
        '''
        HTTP GET Method handler
        '''
        jobs = self.application.pc.get_celery_tasks()

        job_IDs = []
        for job in jobs:
            job_IDs.append(job.id)
            print("executing job with id: ", job.id, flush=True)

        number_ob_jobs = len(jobs)
        if number_ob_jobs > 0:
            return self.finish({
                "data": {
                    "description": "Number of actively running jobs: "+str(number_ob_jobs)+".",
                    "active_jobs": job_IDs
                }
            })
        else:
            return self.finish({"data": "No jobs are actively running at the moment."})


class RevokeJobHandler(web.RequestHandler):
    '''
    RevokeJobHandler allows to stop a running celery process
    Testing: curl -X POST http://localhost:5000/revoke/d9078da5-9915-40a0-bfa1-392c7bde42ed
    '''
    def post(self):
        '''
        HTTP POST Method handler
        '''
        print("inside post request", flush=True)
        json_data = escape.json_decode(self.request.body)
        uuid = json_data["job_uuid"]
        celery.control.revoke(uuid, terminate=True)
        return self.finish({"data": "Revoked job with [uuid] "+uuid+"."})


class CeleryTasks(web.RequestHandler):
    
    @gen.coroutine
    def post(self):

        # preprocessing
        body = escape.json_decode(self.request.body)
        print("[manual job]", flush=True)
        ts = time.time()
        print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], flush=True)
        
        # celery processing start
        future = concurrent.Future()
        if body["task_name"] == "add":
            celery_task = add.delay(3, 3)
        elif body["task_name"] == "manual_task":
            celery_task = manual_task.delay()
        elif body["task_name"] == "manual_task2":
            celery_task = manual_task2.delay()
        elif body["task_name"] == "notify":
            celery_task = notify.delay()
        else:
            celery_task = add.delay(3, 3)
        self.application.pc.add_celery_tasks(celery_task)
        self.check_status(celery_task, future)
        yield future

        ts = time.time()
        print("[event received] epoch: ", ts, ", stamp: ", datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], flush=True)
        return self.finish({"data": "Celery success: "+ str(future.result())}) 


    def check_status(self, celery_task, future):
        """
        Check the status of the celery task and set the result in the future
        """
        if not celery_task.ready():
            ioloop.IOLoop.current().call_later(1, self.check_status, celery_task, future)
        else:
            future.set_result(celery_task.result)
            self.application.pc.remove_celery_tasks(celery_task)


########## periodic tasking
# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

# @celery.task
# def test(arg):
#     print(arg)


########## other configurations

# BROKER_URL = 'mongodb://mongodb:27017/jobs'
# BROKER_URL = 'amqp://user:password@rabbitmq:5672/celeryjobs'
# BROKER_URL = 'redis://redis:6379/0'

# backend='mongodb://mongodb:27017/jobs'
# broker='redis://redis:6379/0'

# # app = Celery('tasks', backend='redis://redis' , broker='amqp://user:password@rabbitmq')
# app = Celery('tasks', backend='redis://redis:6379/0' , broker='redis://redis:6379/0')

# from celery import task

# @task
# def add2(x, y):
#     print("add2 tasks", flush=True)
#     return x + y