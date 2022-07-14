#!/bin/bash

docker-compose down
sleep 5
docker rmi testing_web-ui
# docker rmi testing_response-toolkit
echo "--complete--"
# docker-compose up

