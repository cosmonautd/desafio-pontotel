<template>
<div id="companies-list">
	<b-row align-h="center" align-v="start">
		<h1 class="bovespa-title" style="color: #444">Empresas</h1>
	</b-row>
	<p v-if="$store.state.companies === null || $store.state.companies.length < 1" 
		class="empty-table">
		Empresas não encontradas
	</p>
	<table v-else class="custom-table">
		<tbody>
			<tr v-for="company in $store.state.companies" :key="company.id">
				<td style="width:60%" class="left-round-corners">{{ company.name }}</td>
				<td>{{ company.symbol }}</td>
				<td class="right-round-corners">
					<button @click="companyDetails(company.symbol)" class="round-corners">
						Detalhes
					</button>
				</td>
			</tr>
		</tbody>
	</table>
</div>
</template>

<script>
export default {
	name: "companies-list",
	data() {
		return {
		}
	},
	methods: {
		companyDetails(symbol) {
			this.$router.push({name: 'company_info', params: {symbol}});
		},
		get_companies () {
			this.axios.get(`${process.env.VUE_APP_SERVER_URL}/companies`)
			.then((response) => {
				this.$store.commit('update_companies', response.data.companies)
			})
		},
	},
	mounted() {
		if (this.$store.state.companies === null) {
			this.get_companies()
		}
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