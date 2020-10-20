<template>
<div>
	<div class="yay">
		<b-row align-h="center">
			<div>
				<div class="align-left">
					<p v-if="symbol==='BOVB11.SAO'">
					The Bovespa Index, best known as Ibovespa is the benchmark index of 
					about 70 stocks that are traded on the B3 (Brasil Bolsa Balcão), 
					which account for the majority of trading and market capitalization 
					in the Brazilian stock market. </p>
					<p v-else>
						{{equity_description}}
					</p>
				</div>
			</div>
		</b-row>
		<table class="datatable">
			<tbody>
				<tr>
					<td class="left-round-corners current-value">
						R$ {{current_price}}
					</td>
					<td class="current-others">
						Open <br> {{current_open}}
					</td>
					<td class="current-others">
						High <br> {{current_high}}
					</td>
					<td class="current-others">
						Low <br> {{current_low}}
					</td>
					<td class="current-others">
						Change <br> {{current_change}} ({{current_change_percent}})
					</td>
					<td class="current-others">
						Latest trading day <br> {{latest_trading_day}}
					</td>
					<td class="right-round-corners current-others">
						Last update <br> {{last_update_time}}
					</td>
				</tr>
			</tbody>
		</table>
		<div :style="{visibility: this.loading_data ? 'visible' : 'hidden'}">
			<b-spinner label="Carregando..."></b-spinner>
		</div>
		<line-chart class="padding20" :chart-data="datacollection" :options="options"></line-chart>
		<button class="round-corners" @click="get_data('realtime')">Real time</button>
		<button class="round-corners" @click="get_data('daily')">Daily</button>
		<button class="round-corners" @click="get_data('weekly')">Weekly</button>
		<button class="round-corners" @click="get_data('monthly')">Monthly</button>
	</div>
</div>
</template>

<script>
import LineChart from './LineChart.vue'

export default {
	components: {
		LineChart
	},
	props: {
		symbol: String,
		company_name: String
	},
	computed: {
		current_price () {
			if (this.last_update !== null)
				return this.last_update['price'];
			else return '';
		},
		current_open () {
			if (this.last_update !== null)
				return this.last_update['open'];
			else return '';
		},
		current_high () {
			if (this.last_update !== null)
				return this.last_update['high'];
			else return '';
		},
		current_low () {
			if (this.last_update !== null)
				return this.last_update['low'];
			else return '';
		},
		current_change () {
			if (this.last_update !== null)
				return this.last_update['change'];
			else return '';
		},
		current_change_percent () {
			if (this.last_update !== null){
				let change_percent = this.last_update['change_percent']
				if (change_percent < 0) return `- ${Math.abs(change_percent)}%`;
				else return `+ ${change_percent}%`;
			}
			else return '';
		},
		latest_trading_day () {
			if (this.last_update !== null)
				return this.last_update['latest_trading_day'];
			else return '';
		},
		last_update_time () {
			if (this.last_update !== null)
				return this.last_update['created_at'].substring(0,19);
			else return '';
		}
	},
	data () {
		return {
			datacollection: {labels: [], datasets: []},
			equity_data: {},
			equity_description: '',
			websocket: null,
			period: 'realtime',
			last_update: null,
			loading_data: false,
			options: {
				responsive: true,
				maintainAspectRatio: false,
				layout: {
					padding: 1
				},
				title: {
					// fontSize: 26,
					display: true,
					// text: 'Total confirmed cases'
				},
				scales: {
					xAxes: [{
						ticks: {
							// fontSize: 24
						},
						scaleLabel: {
							display: false,
							labelString: 'Date'
						}
					}],
					yAxes: [{
						type: 'linear',
						scaleLabel: {
							display: true,
							labelString: 'Quote (R$)'
						},
						ticks: {
							// fontSize: 24,
							sampleSize: 6
						}
					}]
				},
				legend: {
					position: 'top',
					labels : {
						fontSize: 18
					},
					display: false
				},
				elements: {
					line: {
						borderWidth: 4
					}
				}
			}
		}
	},
	methods: {
		// https://gist.github.com/glafarge/5bb59d515da551785aff39557a4ab48c
		waitAtLeast(time, promise) {
			const timeoutPromise = new Promise((resolve) => {
				setTimeout(resolve, time);
			});
			return Promise.all([promise, timeoutPromise]).then((values) => values[0]);
		},
		graph_data () {
			if (this.equity_data === null) return [];
			let labels = Object.keys(this.equity_data);
			labels = labels.sort();
			labels = labels.slice(Math.max(labels.length - 40, 0));
			let datapoints = labels.map(label => this.equity_data[label]['price']);
			if (this.period === 'realtime') {
				this.last_update = this.equity_data[labels[labels.length-1]]
				labels = labels.map(label => label.substring(11,16));
			}
			return [labels, datapoints];
		},
		fill_data () {
			let [labels, datapoints] = this.graph_data();
			this.datacollection = {
				labels,
				datasets: [
					{
						label: this.company_name,
						data: datapoints
					}
				]
			}
		},
		get_data (period) {

			this.period = period;
			let promise = null;

			if (period !== 'realtime')
				promise = this.axios.get(`http://localhost:8000/equity/${this.symbol}/${this.period}`);
			else promise = this.axios.get(`http://localhost:8000/equity-realtime/${this.symbol}`);

			if (Object.keys(this.equity_data).length !== 0) {
				this.loading_data = true;
				promise = this.waitAtLeast(600, promise);
			}

			promise.then((response) => {
				this.equity_data = response.data.data;
				this.fill_data();
				this.loading_data = false;
			})
		}
	},
	mounted() {

		this.get_data('realtime')

		let component = this;

		// console.log("Conectando ao websocket")
		this.websocket = new WebSocket(`ws://localhost:8000/quote/realtime/${this.symbol}/ws`)
		this.websocket.onmessage = function(event) {
			if (component.period === 'realtime') {
				let data = JSON.parse(event.data);
				component.equity_data[data.created_at] = data;
				component.fill_data()
			}
		}
		this.websocket.onopen = function() {
			// console.log("Websocket conectado!")
		}
		this.websocket.onclose = function() {
			// console.log("Websocket desconectado!")
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
.padding20 {
	padding: 20px;
}
th {
	text-align: center;
	border-bottom: 0px;
	background-color: #0366ee;
}
td {
	text-align: center;
	border-bottom: 0px;
	background-color: #ffffff;
	opacity: 0.7;
}
.left-round-corners {
	border-radius: 15px 0px 0px 15px;
}
.right-round-corners {
	border-radius: 0px 15px 15px 0px;
}
.yay {
	height: 100%;
	width: 95%;
	margin-left: auto;
	margin-right: auto
}
.datatable {
	margin-top:2em;
}
.current-value {
	font-weight: bold;
	font-size: xx-large;
}
.current-others {
	font-weight: bold;
	font-size: medium;
}
</style>