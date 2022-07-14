<script>
	import axios from "axios";

	let refs1 = [];
	let refs2 = [];

	let dbCollections = {};
	let collection_selected = "";

	let collection_data = [];

	function getDBCollections() {
	    axios.get('/dbcollections').then((response) => {
	    	window.console.log("DBs: ", response.data);
	    	dbCollections = JSON.parse(response.data["return_data"]);
	    	window.console.log(Object.entries(dbCollections))
		}, (error) => {
			window.console.log(error);
		});
	}
	function selectCollection() {
		window.console.log(this);
	}
	function getData() {
		let db_name = "";
		Object.keys(dbCollections).forEach(function(key) {
			if (dbCollections[key].indexOf(collection_selected) > -1) {
				db_name = key;
			}
		});
		if (db_name == "") {
			window.console.log("cannot find database for collection")
			return 
		}
		let data = {"collection_name": collection_selected, "db_name": db_name}
		window.console.log("sending data:", data)
		axios.post(
			'/getdata', 
			data, 
			{'headers': {'Content-Type': 'application/json'}}
		).then((response) => {
			collection_data = response.data["return_data"]
	    	window.console.log("Mongo Data: ", response.data);
		}, (error) => {
			window.console.log(error);
		});
	}
	function deleteData() {
		let db_name = "";
		Object.keys(dbCollections).forEach(function(key) {
			if (dbCollections[key].indexOf(collection_selected) > -1) {
				db_name = key;
			}
		});
		if (db_name == "") {
			window.console.log("cannot find database for collection")
			return 
		}
		let data = {"collection_name": collection_selected, "db_name": db_name}
		axios.post(
			'/deletedata', 
			data, 
			{'headers': {'Content-Type': 'application/json'}}
		).then((response) => {
			collection_data = [];
	    	window.console.log("Response: ", response.data);
		}, (error) => {
			window.console.log(error);
		});
	}
</script>

<hr>

<div class="w3-panel w3-blue">
  <h1 class="w3-text-yellow" style="text-shadow:1px 1px 0 #444">
  <b>Databases and Collections</b></h1>
</div>
<!-- <h5>Databases and Collections</h5> -->

<button class="w3-col w3-input w3-border" on:click={getDBCollections}>DBs and Collections</button>

<br>

{#each Object.entries(dbCollections) as [title, collections]}
	<div class="db-name">{title}</div>
	<ul>
		{#each collections as item, index}
			<li class="db-collection" bind:this={refs1[index]}>
				{item}
			</li>
		{/each}
		<br>
	</ul>
{/each}

<hr>

<div class="w3-panel w3-blue">
  <h1 class="w3-text-yellow" style="text-shadow:1px 1px 0 #444">
  <b>Collection Data</b></h1>
</div>
<!-- <h5>Show Collection Data</h5> -->

<div class="w3-row w3-section">
    <div class="w3-third">
        <!-- <input id="renameScenario" class="w3-input w3-border" name="name" type="text" placeholder="Scenario Name"> -->
        <input bind:value={collection_selected} class="w3-input w3-border" type="text" placeholder="collection_name">
    </div>
    <div class="w3-third">
        <button on:click={getData} class="w3-col w3-input w3-border">Get Data</button>
    </div>
    <div class="w3-rest">
        <button on:click={deleteData} class="w3-col w3-input w3-border" >Clear Data</button>
    </div>
</div>

<ul>
	{#each collection_data as item, index}
		<li bind:this={refs2[index]}>
			{JSON.stringify(item, undefined, 2)}
		</li>
	{/each}
</ul>


<style>
	.db-name {
		text-align: left;
		font-weight: bold;
	}
	.db-collection {
		text-align: left;
	}
	hr {
		color: white;
		border-top: 1px solid white;
	}
</style>
