import requests


def certh(payload):
    url = "http://160.40.49.152:8091/response-agent/iptables"
    r = requests.post(url, json=payload)
    return r

def local_agent(payload):
    url = "http://response-agent:8888/response"
    # payload determines actions (shutdown, stopping vehicle, reconfigure)
    r = requests.post(url, json=payload)
    return r

def recovery_toolkit(payload):
    url = "http://recovery-toolkit:5004/"
    # payload determines actions (process, device, or functionality restart)
    r = requests.post(url, json=payload)
    return r
