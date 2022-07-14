## Intrusion Response Toolkit

to see how the toolkit is being used, either watch the video provided in the root folder of this repository or read and test the documentation below.

- start toolkit by jumping into the root folder and executing `docker-compose up`
- connect to the frontend of the toolkit by using the browser and the url `localhost:5001`
- to connect to the rabbitMQ, use the tab of the frontend and login with the credentials `user` and `password`
- in the rabbit UI, you can inspect all connections, queues, channels, exchanges, etc.
- the swagger API is reachable via another UI tab but is kept at a minimum description
- to use the toolkit:
		- NOTIFY TASK: 
			- for running the task notify, write `notify` into the manual response strategy field and hit `Execute Manual Response`
			- next go to the database tab and copy the job collection name and past it into the string field below and click `get data`, this shows successfull invocations of notify.
		- MANUAL TASK:
			- sends data to the response toolkit, write `manual_task` into the manual task field. the action fails if the response toolkit is offline.
		- REVOCATION OF TASK:
			- start a the manual task by writing `add` into the field. above in the monitoring of active response, you can see the job id. the add task runs for 15 seconds and is executed by a celery worker. to revoke the task, simply copy paste the job ID of the task into the revocation field in under manual response.
		- AUTOMATED RESPONSE:
			- to launch an automated response, click on `Sample 1` or `Sample 2` under the field `Automatic Response Strategies`
			- next click the yellow submit button to launch an automated response. the response will be handles asynchronously by celery workers and results are recorded in the database. rabbitMQ message brokers take over the task queueing and monitor/manage responses between the backend and the celery workers.
			- the output is visible in the event logs section below.

- possible tasks are: manual_task, notify, automated_task, add2, add, 
- other tasks can be added in the response-toolkit folder under the file `tasks.py`

## docker connection string

- `mongo admin -u user -p "password"`

#### Webserver stack
- container running the tornado webserver serving vue js frontend application
- portainer container setup to monitor docker containers via the UI

#### RabbitMQ
Message broker for celery distributed tasking application on the containers

#### Redis
Storing results of distributed tasking via celery in containers

#### Data generator
Running and exposing software modules via REST API
- by calling the rest API it is possible to see the tools that can be executed in a celery process

Celery:
start worker: `celery -A tasks worker --loglevel=info`

## licenses
celerybeat-mongo: Apache-2.0 License
celery: BSD-3-Clause License 
tornado: Apache-2.0 License
pymongo: Apache-2.0 License
redis: BSD-3-Clause License
pika: BSD-3-Clause License
requests: Apache-2.0 License

### evaluation
- local client autoamted requests:
	10:  11:18:26.972  11:18:28.015
	20: 

