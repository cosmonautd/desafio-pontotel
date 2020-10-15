<template>
<div class="small">
	<line-chart class="padding30" :chart-data="datacollection"></line-chart>
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
			company_data: null
		}
	},
	props: {
		symbol: String
	},
	computed: {
		labels () {
			if (this.company_data === null) return []
			return Object.keys(this.company_data).sort() // Rever essa operação
		},
		datapoints () {
			if (this.company_data === null) return []
			let points = []
			for (let date of Object.keys(this.company_data).sort()) { // Rever também
				points.push(this.company_data[date]['close'])
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
						label: `Cotação ${this.symbol}`,
						data: this.datapoints
					}
				]
			}
		},
		get_data (period) {
			this.axios.get(`http://localhost:8000/company/${this.symbol}/${period}`)
			.then((response) => {
				this.company_data = response.data.data
				this.fill_data()
			})
		}
	},
	mounted() {
		this.get_data('daily')
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