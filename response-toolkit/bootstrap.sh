#!/bin/sh

sleep 15

# turn on bash's job control
# set -m


# Start the helper process
celery -A tasks worker --loglevel=info --concurrency=2 & # "-B" flags sets the beat service into this worker
  
#-B -E --concurrency=4
# Start the primary process and put it in the background
python3 main.py 
  
# celery -A tasks beat
# celery -A tasks beat -S celerybeatmongo.schedulers.MongoScheduler -l info

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns
    
# now we bring the primary process back into the foreground
# and leave it there
# fg %1
