import time
import datetime
import uuid

ts = time.time()

# event definition
ERROR_NOT_EXIST = {
    "event_type": "error",
    "niove_module": "response-toolkit",
    "input_event": {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "type": ""
    },
    "response": None,
    "status": "service does not exist",
    "epoch": ts,
    "time_stamp": datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    "uuid": str(uuid.uuid4())
}


ERROR_PROCESSING = {
    "event_type": "error",
    "niove_module": "response-toolkit",
    "input_event": {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "type": ""
    },
    "response": None,
    "actions": None,
    "status": "pre-processing failed",
    "epoch": ts,
    "time_stamp": datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    "uuid": str(uuid.uuid4())
}

ERROR_INTERNAL = {
    "event_type": "error",
    "niove_module": "response-toolkit",
    "input_event": {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "type": ""
    },
    "response": {
        "selection": "static", # static•automated
        "nature": "active", # active•passive
        "time": "delayed", # delayed•proactive
        "degree": "manual" # manual•automated
    },
    "actions": [{
        "action": "HTTP request",
        "service": "block IP address",
        "target": {
            "name": "response agent",
            "uuid": "00000000-0000-0000-0000-000000000000",
            "ip": "127.0.0.1",
            "policy": "block" # block•recover•normal
        }
    }],
    "status": "internal error",
    "epoch": ts,
    "time_stamp": datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    "uuid": str(uuid.uuid4())
}


EVENT_RECEIVED = {
    "event_type": "notification",
    "niove_module": "response-toolkit",
    "input_event": {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "type": ""
    },
    "response": None,
    "actions": None,
    "status": "pre-processing", # running•idle
    "epoch": ts,
    "time_stamp": datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    "uuid": str(uuid.uuid4())
}


EVENT_INTERMEDIATE = {
    "event_type": "notification",
    "niove_module": "response-toolkit",
    "input_event": {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "type": ""
    },
    "response": {
        "selection": "static", # static•automated
        "nature": "active", # active•passive
        "time": "delayed", # delayed•proactive
        "degree": "manual" # manual•automated
    },
    "actions": [{
        "action": "HTTP request",
        "service": "block IP address",
        "target": {
            "name": "response agent",
            "uuid": "00000000-0000-0000-0000-000000000000",
            "ip": "127.0.0.1",
            "policy": "block" # block•recover•normal
        }
    }],
    "status": "running", # running•idle
    "epoch": ts,
    "time_stamp": datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    "uuid": str(uuid.uuid4())
}


EVENT_COMPLETED = {
    "event_type": "notification",
    "niove_module": "response-toolkit",
    "input_event": {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "type": ""
    },
    "response": {
        "selection": "static", # static•automated
        "nature": "active", # active•passive
        "time": "delayed", # delayed•proactive
        "degree": "manual" # manual•automated
    },
    "actions": [{
        "action": "HTTP request",
        "service": "block IP address",
        "target": {
            "name": "response agent",
            "uuid": "00000000-0000-0000-0000-000000000000",
            "ip": "127.0.0.1",
            "policy": "block" # block•recover•normal
        }
    }],
    "result": None,
    "status": "succeeded", # pre-processing•running•succeeded•failed•idle
    "epoch": ts,
    "time_stamp": datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    "uuid": str(uuid.uuid4())
}


# expecting to receive:
# {
#     "uiid":"793b8add-184d-489b-8f30-39527fe7f3b7",
#     "type":"DDOS attack",
#     "taxonomy":["infrastructure layer", "SYN flood", "TCP"],
#     "timestamp_started":"2020-09-03 00:43:35.520",
#     "timestamp_finished":"2020-09-03 03:17:21.116",
#     "severity":"5",
#     "sources":["6.139.209.173","43.118.93.222","122.45.38.175"],
#     "targets":[{"uuid":"80e73532-52c2-4b57-affe-47afffc5e6b3","ip":"172.17.0.5"}]
# }

