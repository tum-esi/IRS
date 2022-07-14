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


<h5>Databases and Collections</h5>

<button on:click={getDBCollections}>DBs and Collections</button>

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

<br>
<h5>Show Collection Data</h5>
<input bind:value={collection_selected} class="input" type="text" placeholder="collection_name">
<br>
<button on:click={getData}>Get Data</button>
<button on:click={deleteData}>Delete Data</button>
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
</style>
