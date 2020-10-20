<template>
<div id="company-info" :key="generateUniqueKey()">
	<div class="vertical-spacing-1"></div>
	<div class="vertical-spacing-top"/>
	<b-container fluid class="bv-example-row">
		<b-row align-h="center" style="height: 100%;">
			<b-col xs="10" sm="10" md="10" lg="10" xl="10" align-self="center">
				<b-row align-h="center" align-v="start">
					<h1 class="bovespa-title" style="color: #444">
						{{company_name}} ({{$route.params.symbol}})
					</h1>
				</b-row>
			</b-col>
			<b-col sm="12" md="12" lg="12" xl="12">
				<Chart :symbol="$route.params.symbol" :company_name="company_name"/>
			</b-col>
		</b-row>
	</b-container>
</div>
</template>

<script>
import Chart from "./Chart.vue";
export default {
	name: "company-info",
	components: {
		Chart
	},
	data () {
		return {
			company: null
		}
	},
	computed: {
		company_name () {
			if (this.$store.state.companies === null) return '';
			else {
				let company = this.$store.state.companies.filter(
					c => c.symbol === this.$route.params.symbol
				)[0];
				return company.name;
			}
		}
	},
	methods: {
		get_company (symbol) {
			this.axios.get(`http://localhost:8000/company/${symbol}`)
			.then((response) => {
				this.company = response.data.company;
			})
		},
		generateUniqueKey() {
			return Date.now().toString();
		}
	},
	mounted () {
		this.get_company(this.$route.params.symbol);
	}
}
</script>

<style scoped>
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
table {
	border-collapse: separate; 
	border-spacing: 0 1em;
}
.left-round-corners {
	border-radius: 15px 0px 0px 15px;
}
.right-round-corners {
	border-radius: 0px 15px 15px 0px;
}
</style>