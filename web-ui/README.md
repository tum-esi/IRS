## Tornado webserver with Celery


#### using pipenv as the python package manager
#### using python 3.7 or higher

#### local testing
- make sure to set up the docker containers for redis and rabbitmq
- (https://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#rabbitmq)
- `docker run -d -p 6379:6379 redis`
- `docker run -d -p 5672:5672 rabbitmq`


