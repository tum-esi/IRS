<script>
	import axios from "axios";
	import { onMount } from 'svelte';
	import {link} from 'svelte-spa-router'

	let incident_number = 0;
    let incident_data = "";
    let channel = "security_incident";
    let data_size0 = 0;
    let data_size1 = 0;
    let data_size2 = 0;
    let results = ["event1", "event2", "event3"];
    let refs = [];
    let count = 1;
    let array_counter = 0;

    let sampleJSON = {
    	"uuid":"793b8add-184d-489b-8f30-39527fe7f3b7",
		"type":"DDOS attack",
		"taxonomy":["infrastructure layer", "SYN flood", "TCP"],
		"timestamp_started":"2020-09-03 00:43:35.520",
		"timestamp_finished":"2020-09-03 03:17:21.116",
		"severity":"5",
		"sources":[
		    "6.139.209.173",
		    "43.118.93.222",
		    "122.45.38.175"
		],
		"targets":[{
		    "uuid":"80e73532-52c2-4b57-affe-47afffc5e6b3",
		    "ip":"172.17.0.5"
		}]
	};

	let response_call_timing = "";
    function handleSubmit() {
		console.log("Submit");

		let d = new Date().toISOString()
		window.console.log(d, ", Submit of CERTH response format :)")

		array_counter = 0;

		// let json_data = JSON.parse(JSON.stringify(incident_data))
		let json_data = JSON.parse(incident_data)
		let data = {
			"incident_number": incident_number,
			"incident_data": json_data,
			"channel": channel
		}

		window.console.log("printing data: ", data);

		axios.post('/evaluate_rtk', data, {
			'headers': {'Content-Type': 'application/json'}
		}).then((response) => {
			window.console.log(response);
		}, (error) => {
			window.console.log(error);
		});
	}
	function handleClear() {
		console.log("Clear");
	}
	function pasteTxT() {
		incident_data = JSON.stringify(sampleJSON, undefined, 4);
	}
	function clearTxT() {
		incident_data = "";
	}
	function prettyPrint() {
		let obj = JSON.parse(incident_data);
    	incident_data = JSON.stringify(obj, undefined, 4);
	}
	function newSize() {
		const size = new TextEncoder().encode(JSON.stringify(incident_data)).length;
		const kiloBytes = size / 1024;
		const megaBytes = kiloBytes / 1024;
		data_size0 = size;
		data_size1 = kiloBytes;
		data_size2 = megaBytes;
	}
	function clearEvents() {
		results = ["event1", "event2", "event3"];
	}

	let led_green = 'led-green2';
	let led_red = 'led-red2';
	let status_message = "Job Status";
	let response_services = "dummy service";

	// executed when component mounted
	onMount(async () => {

		// websocket connection
	    let ws = new WebSocket("ws://localhost:5001/response/ws");
	    ws.onopen = function() {
	      window.console.log("Successfully connected to the echo websocket server...");
	    };
	    ws.onmessage = function(evt) {
	      window.console.log(evt, "adding to results");
	      results[array_counter] = evt.data;
	      array_counter += 1;
	      // results.push(evt.data);
	    };

	    setTimeout(function(){ 
	    	window.console.log("sleep 1 sec.")
    	}, 1000);

	    // fetch services of response module
	    axios.get('/services').then((response) => {
	    	window.console.log("services", response.data);
			response_services = response.data["return_data"];
		}, (error) => {
			window.console.log(error);
		});

	    // interval requests
		setInterval(function(){ 
			// heartbeat
			axios.get('/heartbeat').then(() => {
				led_green = 'led-green';
				led_red = 'led-red2';
			}, () => {
				led_green = 'led-green2';
				led_red = 'led-red';
			});
			// processing status
			axios.get('/status').then((response) => {
				window.console.log("services", response.data);
				status_message = response.data["return_data"];
			}, (error) => {
				window.console.log("error fetching status information");
			});
		}, 2000);

	});

	let task_name = ""
	function postManualResponse() {

		let data = {"task_name": task_name};
		
		let d = new Date().toISOString()
		window.console.log(d, ", regular post request")
		
		const t0 = performance.now();
		axios.post('/job', data, {
			'headers': {'Content-Type': 'application/json'}
		}).then((response) => {
			const t1 = performance.now();
			console.log(`Call to doSomething took ${t1 - t0} milliseconds.`);
			window.console.log(response.data);
		}, (error) => {
			window.console.log(error);
		});
	}

	let uuid = "";
	function postRevokeResponse() {
		// const millis1 = Date.now();
		// window.console.log(`revoke seconds elapsed = ${Math.floor(millis1 / 1000)}`);
		let d = new Date().toISOString()
		window.console.log(d, ", right format :)")
		
		let data = {"job_uuid": uuid};
		axios.post('/revoke', data, {
			'headers': {'Content-Type': 'application/json'}
		}).then((response) => {
			window.console.log(response);
		}, (error) => {
			window.console.log(error);
		});
	}

</script>

<div>
	<a href="http://localhost:5000/doc">|| Response Toolkit Swagger API |</a>
	<a href="http://localhost:15672/">| RabbitMQ Message Broker |</a>
	<a href="/mongo" use:link>| Results Database |</a>
	<a href="/messages" use:link>| Sample JSON Security Incidents ||</a>
</div>
<h3>Response Toolkit Evaluation</h3>

<h5>Activity Status</h5>

<div class="container activity">
	<div class="led-box">
	    <div class="{led_green}"></div>
	    <p>Active</p>
	  </div>

	<div class="led-box">
	    <div class="{led_red}"></div>
	    <p>Inactive</p>
	</div>
</div>
<div>{JSON.stringify(status_message, undefined, 4)}</div>

<h5>Existing Services of Response Toolkit</h5>
<div>{JSON.stringify(response_services, undefined, 4)}</div>

<h5>Manual Toolkit Requests</h5>

<div class="container activity">
	possible task_name s: add (default), manual_task, notify 
	<input bind:value={task_name} class="input" type="text" placeholder="task_name">
	<button on:click={postManualResponse}>Response Action</button>

	<div>
		<input bind:value={uuid} class="input" type="text" placeholder="00000000-0000-0000-0000-000000000000">
		<button on:click={postRevokeResponse}>Revoke Action</button>
	</div>
</div>

<h5>Automated Toolkit Requests via Message Broker</h5>

<div class="row">
  
	<div class="column" style="background-color:#ccc;">
	    <div>number of messages</div>
		<input bind:value={incident_number} class="input" type="number">
		<br>
		<div>RabbitMQ Channel</div>
		<select>
			<option selected>{channel}</option>
		</select>
		<br>
		<div>Input to send to RabbitMQ</div>
		<textarea class="textarea" placeholder="Textarea" type="text" bind:value={incident_data}></textarea>
		<br>
		<button on:click={prettyPrint}>Pretty Print</button>
		<button on:click={clearTxT}>Clear</button>
		<br>

		<div>JSON Message sizes</div>
		<div>{ data_size0 } in Bytes (B), { data_size1 } in kiloBytes (kB), { data_size2 } in megaBytes (MB)</div>
		<!-- <div>{ data_size1 } in kiloBytes (kB)</div>
		<div>{ data_size2 } in megaBytes (MB)</div> -->

		<button on:click={newSize}>Get Sizes</button>
	</div>

	<div class="column" style="background-color:#ccc;">
		<p>{JSON.stringify(sampleJSON, undefined, 4)}</p>
		<br>
		<button on:click={pasteTxT}>Copy into textarea</button>
		<br>
		<br>
		<br>
		<button on:click={handleSubmit}>
			Submit
		</button>
		<button on:click={handleClear}>
			Clear
		</button>
	</div>
</div>

<h5>Timing Results</h5>


<h5>Result Events</h5>

<button on:click={clearEvents}>Clear Events</button>

<ul>
	{#each results as item, index}
		<li bind:this={refs[index]}>
			{item}
		</li>
	{/each}
</ul>

<br>
<br>



<style>
	.led-green {
		margin: 0 auto;
		width: 24px;
		height: 24px;
		background-color: #ABFF00;
		border-radius: 50%;
		box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #304701 0 -1px 9px, #89FF00 0 2px 12px;
	}
	.led-green2 {
		margin: 0 auto;
		width: 24px;
		height: 24px;
		background-color: #ABFF00;
		border-radius: 50%;
		/*box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #304701 0 -1px 9px, #89FF00 0 2px 12px;*/
	}
	.led-red {
		margin: 0 auto;
		width: 24px;
		height: 24px;
		background-color: #F00;
		border-radius: 50%;
		box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 12px;
		-webkit-animation: blinkRed 1.5s infinite;
		-moz-animation: blinkRed 1.5s infinite;
		-ms-animation: blinkRed 1.5s infinite;
		-o-animation: blinkRed 1.5s infinite;
		animation: blinkRed 1.5s infinite;
	}
	.led-red2 {
		margin: 0 auto;
		width: 24px;
		height: 24px;
		background-color: #F00;
		border-radius: 50%;
		/*box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 12px;*/
	}
	.activity {
		display: flex;
		justify-content: space-around;
	}

	@-webkit-keyframes blinkRed {
		from { background-color: #F00; }
		50% { background-color: #A00; box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 0;}
		to { background-color: #F00; }
	}
	@-moz-keyframes blinkRed {
		from { background-color: #F00; }
		50% { background-color: #A00; box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 0;}
		to { background-color: #F00; }
	}
	@-ms-keyframes blinkRed {
		from { background-color: #F00; }
		50% { background-color: #A00; box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 0;}
		to { background-color: #F00; }
	}
	@-o-keyframes blinkRed {
		from { background-color: #F00; }
		50% { background-color: #A00; box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 0;}
		to { background-color: #F00; }
	}
		@keyframes blinkRed {
		from { background-color: #F00; }
		50% { background-color: #A00; box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px, rgba(255, 0, 0, 0.5) 0 2px 0;}
		to { background-color: #F00; }
	}
	textarea, input, select {
		width: 300px;
		max-width: 300px;
		max-height: 95px;
	}

	* {
	  box-sizing: border-box;
	}
	h5 {
		text-align: left;
	}
	.row {
	  display: flex;
	}

	/* Create two equal columns that sits next to each other */
	.column {
	  flex: 50%;
	  padding: 10px;
	  height: 350px; /* Should be removed. Only for demonstration */
	}
</style>
