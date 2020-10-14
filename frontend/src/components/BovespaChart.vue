<template>
<div class="small">
	<line-chart class="padding30" :chart-data="datacollection"></line-chart>
	<button class="round-corners" @click="fill_data()">Randomize</button>
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
			bovespa_data: null
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
				points.push(this.bovespa_data[date]['close'])
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
		}
	},
	mounted() {
		this.axios.get('http://localhost:8000/bovespa/daily')
		.then((response) => {
			this.bovespa_data = response.data.data
			this.fill_data()
		})
	},
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