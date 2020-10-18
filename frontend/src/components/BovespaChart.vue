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
	data () {
		return {
			datacollection: null,
			bovespa_data: null,
			websocket: null
		}
	},
	computed: {
		labels () {
			if (this.bovespa_data === null) return []
			return Object.keys(this.bovespa_data).sort() // Rever essa operação
		},
		datapoints () {
			if (this.bovespa_data === null) return []
			let points = []
			for (let date of Object.keys(this.bovespa_data).sort()) { // Rever também
				points.push(this.bovespa_data[date]['price'])
			}
			return points
		}
	},
	methods: {
		fill_data () {
			this.datacollection = {
				labels: this.labels,
				datasets: [
					{
						label: 'Índice Bovespa',
						data: this.datapoints
					}
				]
			}
		},
		get_data (period) {
			this.axios.get(`http://localhost:8000/equity/BOVB11.SAO/${period}`)
			.then((response) => {
				this.bovespa_data = response.data.data
				this.fill_data()
			})
		}
	},
	mounted() {

		this.get_data('realtime')

		console.log("Conectando ao websocket")
		this.websocket = new WebSocket('ws://localhost:8000/ws')
		this.websocket.onmessage = function(event) {
			console.log(event.data);
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