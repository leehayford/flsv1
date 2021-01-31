<script>
	// export let name;
	export let depth;
	export let tension;
	export let speed;
	export let ccl;
	export let gr;
	export let temp;
	export let press;
	export let flowUp;
	export let flowDn;
	export let spinner;

	var socket = io();
	socket.on('connect', function() {
		console.log('\n[*** CONNECTED ***]\nconnected - svelte')
		socket.emit('getsimdata',  'svelte client ready for data....\n' );
	});
	socket.on('newdata', function(djson) {
		var d = JSON.parse(djson);
		// console.log('\n[*** NEW DATA RECEIVED ***]\n', d['depth'])
		depth = d['depth'];
		tension = d['tension'];
		speed = d['speed'];
		ccl = d['ccl'];
		gr = d['gr'];
		temp = d['temp'];
		press = d['press'];
		flowUp = d['flowUp'];
		flowDn = d['flowDn'];
		spinner = d['spinner'];
	});
</script>

<main>
	<h1>Sup?</h1>
	<p>depth: {depth}</p>
	<p>tension: {tension}</p>
	<p>speed: {speed}</p>
	<p>ccl: {ccl}</p>
	<p>gr: {gr}</p>
	<p>temp: {temp}</p>
	<p>press: {press}</p>
	<p>flowUp: {flowUp}</p>
	<p>flowDn: {flowDn}</p>
	<p>spinner: {spinner}</p>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
