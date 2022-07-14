<script>
	import { page } from '$app/stores';

	function myFunction() {
		var x = document.getElementById("demo");
		if (x.className.indexOf("w3-show") == -1) {
			x.className += " w3-show";
		} else { 
			x.className = x.className.replace(" w3-show", "");
		}
	}

</script>

<header>
	<div class="w3-bar w3-blue">
		<a href="/" class:active={$page.path === '/'} class="w3-bar-item w3-button">Home</a>
		<a href="/strategies" class:active={$page.path === '/strategies'} class="w3-bar-item w3-button w3-hide-small">Strategies</a>
		<a href="/database" class:active={$page.path === '/database'} class="w3-bar-item w3-button w3-hide-small">Database</a>
		<a href="http://localhost:15672/" class="w3-bar-item w3-button w3-hide-small">Rabbit Broker</a>
		<a href="http://localhost:5000/doc" class="w3-bar-item w3-button w3-hide-small">Swagger API</a>
		<button class="w3-bar-item w3-button w3-right w3-hide-large w3-hide-medium" on:click={myFunction}>&#9776;</button>
	</div>

	<div id="demo" class="w3-bar-block w3-blue w3-hide w3-hide-large w3-hide-medium">
		<a href="/" class:active={$page.path === '/'} class="w3-bar-item w3-button">Home</a>
		<a href="/strategies" class:active={$page.path === '/strategies'} class="w3-bar-item w3-button">Strategies</a>
		<a href="/database" class:active={$page.path === '/database'} class="w3-bar-item w3-button">Database</a>
		<a href="http://localhost:15672/" class="w3-bar-item w3-button">Rabbit Broker</a>
		<a href="http://localhost:5000/doc" class="w3-bar-item w3-button">Swagger API</a>
	</div>
</header>

<style>

	a.active {
		color: yellow;
	}

</style>
