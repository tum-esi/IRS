<script context="module">
	export const prerender = true;

	let imgsrc = '/D5.3-sstack.png'
</script>

<script>
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<section>
	<h1>
		<div class="w3-container w3-margin">
			nIoVe Response Toolkit
		</div>

		<div class="w3-container">
			<img class="w3-round w3-padding-48" src={imgsrc} alt="Welcome" />
		</div>
	</h1>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 1;
	}

	h1 {
		width: 100%;
	}

</style>
