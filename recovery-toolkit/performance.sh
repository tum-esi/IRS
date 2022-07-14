#!/bin/bash

start_time=$(($(date +%s%N)/1000000))
# echo "sleep 1 second"
# sleep 1
# echo "wake up"

# execute command to measure

# 1.
# docker commit recovery-toolkit_recovery-toolkit_1 recovery_image:1.0
# 2.
# docker save --output niove_recover.tar recovery_image:1.0
# 3.
# docker load --input niove_recover.tar
# 4.
# curl -F "userid=1" -F "filecomment=This is an tar file" -F "tar=@/home/jp/Documents/coding/gitlab.com/WP5-response-toolkit-TUM/testing/recovery-toolkit/niove_recover.tar" localhost:5000/upload-checkpoint
# 5. make sure to collect object id by manually connecting to gridfs over mongo container
# curl --header "Content-Type: application/json" --request POST -o recovery-test.tar --data '{"file_id":"6027241a2ffce167a3e37e5f"}' http://localhost:5000/checkpoint-rollback 2> error-recovery.txt

# fetch data down...

end_time=$(($(date +%s%N)/1000000))

echo "execution took:" $(($end_time - $start_time)) "ms"


# 1. command result in ms: 1011 ms, with image size: 57.6MB, container info: "ShmSize": 67108864
# as reference, default python image has a size of 41.8MB (python:3.7-alpine)

# 2. command result in ms: 2427 ms, tar file has size: 58M in total

# 3. command result in ms: 362 ms, image in between: 
# jp@jplenovo> ./performance.sh                                                                      ~/Documents/coding/gitlab.com/WP5-response-toolkit-TUM/testing/recovery-toolkit
# 7cf8ea7821c2: Loading layer [==================================================>]  354.3kB/354.3kB
# Loaded image: recovery_image:1.0
# execution took: 362 ms

# 4. command result in ms: 27451 ms
# jp@jplenovo> ./performance.sh
# {"gridfs_id": "60272040ecf37fa8e9964ee5", "filename": "test.tar"}execution took: 27451 ms

# 5. command result in ms: 470 ms

