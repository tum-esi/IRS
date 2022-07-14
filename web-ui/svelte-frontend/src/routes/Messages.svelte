<script>
	
	let msg1 = {
		"uuid": "",
		"type": "",
		"taxonomy": [],
		"timestamp_started": "",
		"timestamp_ended": "",
		"severity": "",
		"sources": [{}],
		"targets": [
		{
		  "ip": "",
		  "uuid": ""
		}
		],
		"possible_targets": [
		{
		  "ip": "",
		  "uuid": ""
		},
		{
		  "ip": "",
		  "uuid": ""
		}
		]
	};

	let msg2 = {
	  "uuid": "793b8add-184d-489b-8f30-39527fe7f3b7",
	  "type": "DDOS attack",
	  "taxonomy": [
	    "infrastructure layer",
	    "SYN flood",
	    "TCP"
	  ],
	  "timestamp_started": "2020-09-03 00:43:35.520",
	  "timestamp_ended": "2020-09-03 03:17:21.116",
	  "severity": "5",
	  "sources": [
	    {
	      "ip": "6.139.209.173"
	    },
	    {
	      "ip": "43.118.92.222"
	    },
	    {
	      "ip": "122.45.38.175"
	    }
	  ],
	  "targets": [
	    {
	      "ip": "172.17.0.5",
	      "uuid": "588e188c-5c0d-11eb-ae93-0242ac130002"
	    }
	  ],
	  "possible_targets": [
	    {
	      "ip": "172.17.0.7",
	      "uuid": "4d394c0e-5c0d-11eb-ae93-0242ac130002"
	    },
	    {
	      "ip": "172.17.0.8",
	      "uuid": "a5f68186-5c0d-11eb-ae93-0242ac130002"
	    }
	  ]
	}

	let msg3 = {
	  "uuid": "5f5aee7f-3899-4218-b887-acba844e2fa4",
	  "type": "MITM attack",
	  "taxonomy": [
	    "false message attack"
	  ],
	  "timestamp_started": "2020-09-07 08:25:14.014",
	  "timestamp_ended": "2020-09-07 08:26:01.005",
	  "severity": "5",
	  "sources": [],
	  "targets": [
	    {
	      "ip": "172.17.0.5",
	      "uuid": "588e188c-5c0d-11eb-ae93-0242ac130002"
	    },
	    {
	      "ip": "172.17.0.7",
	      "uuid": "4d394c0e-5c0d-11eb-ae93-0242ac130002"
	    }
	  ],
	  "possible_targets": [
	    {
	      "ip": "172.17.0.3",
	      "uuid": "085f2ee2-6f92-4a71-94ef-8b96ff5faa15"
	    },
	    {
	      "ip": "172.17.0.6",
	      "uuid": "364afd20-e18b-4a43-b281-162543fb95c3"
	    },
	    {
	      "ip": "172.17.0.8",
	      "uuid": "a5f68186-5c0d-11eb-ae93-0242ac130002"
	    }
	  ]
	}

	let msg4 = {
	  "uuid": "",
	  "event_type": "",
	  "niove_module": "",
	  "response": {
	    "type": "",
	    "target": ""
	  },
	  "state": ""
	}

	let msg5 = {
	  "uuid": "793b8add-184d-489b-8f30-39527fe7f3b7", 
	  "event_type": "notification", 
	  "niove_module": "response-toolkit", 
	  "response": null, 
	  "state": "preprocessing"
	}

	let msg6 = {
	  "uuid": "793b8add-184d-489b-8f30-39527fe7f3b7",
	  "event_type": "process",
	  "niove_module": "response-toolkit",
	  "response": {
	    "type": "static",
	    "target": "172.18.0.9"
	  },
	  "state": "succeeded"
	}

</script>


<h3>Messages</h3>

<p>{JSON.stringify(msg1, undefined, 2)}</p>
<p>{JSON.stringify(msg2, undefined, 2)}</p>
<p>{JSON.stringify(msg3, undefined, 2)}</p>
<p>{JSON.stringify(msg4, undefined, 4)}</p>
<p>{JSON.stringify(msg5, undefined, 4)}</p>
<p>{JSON.stringify(msg6, undefined, 4)}</p>

