<template>
<div class="small">
	<line-chart class="padding30" :chart-data="datacollection"></line-chart>
	<button class="round-corners" @click="get_data('realtime')">Atual</button>
	<button class="round-corners" @click="get_data('daily')">Diário</button>
	<button class="round-corners" @click="get_data('weekly')">Semanal</button>
	<button class="round-corners" @click="get_data('monthly')">Mensal</button>
</div>
</template>

<script>
import LineChart from './LineChart.vue'

export default {
	components: {
		LineChart
	},
	props: {
		symbol: String
	},
	data () {
		return {
			datacollection: {labels: [], datasets: []},
			bovespa_data: null,
			websocket: null,
			period: 'realtime'
		}
	},
	methods: {
		graph_data () {
			if (this.bovespa_data === null) return [];
			let labels = Object.keys(this.bovespa_data);
			labels = labels.sort();
			labels = labels.slice(Math.max(labels.length - 40, 0));
			let datapoints = labels.map(label => this.bovespa_data[label]['price']);
			if (this.period === 'realtime')
				labels = labels.map(label => label.substring(11,16));
			return [labels, datapoints];
		},
		fill_data () {
			let [labels, datapoints] = this.graph_data();
			this.datacollection = {
				labels,
				datasets: [
					{
						label: this.symbol,
						data: datapoints
					}
				]
			}
		},
		get_data (period) {
			this.period = period
			this.axios.get(`http://localhost:8000/equity/${this.symbol}/${this.period}`)
			.then((response) => {
				this.bovespa_data = response.data.data
				this.fill_data()
			})
		}
	},
	mounted() {

		this.get_data('realtime')

		let component = this;

		console.log("Conectando ao websocket")
		this.websocket = new WebSocket(`ws://localhost:8000/quote/realtime/${this.symbol}/ws`)
		this.websocket.onmessage = function(event) {
			let data = JSON.parse(event.data);
			component.bovespa_data[data.created_at] = data;
			component.fill_data()
		}
		this.websocket.onopen = function() {
			console.log("Websocket conectado!")
		}
		this.websocket.onclose = function() {
			console.log("Websocket desconectado!")
		}
	},
	beforeDestroy() {
		this.websocket.close()
	}
}
</script>

<style scoped>
.small {
	max-width: 600px;
	margin:  25px auto;
}
.padding30 {
	padding: 30px;
}
</style>