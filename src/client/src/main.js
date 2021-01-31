// import Speedometer from"svelte-speedometer"
import App from './App.svelte';

const app = new App({
	target: document.body,
	props: {
		depth: 0.0,
		tension: 0.0,
		speed: 0.0,
		ccl: 0.0,
		gr: 0.0,
		temp: 0.0,
		press: 0.0,
		flowUp: 0.0,
		flowDn: 0.0,
		diffPress: 0.0,
		spinner: 0.0
	}
});

export default app;
