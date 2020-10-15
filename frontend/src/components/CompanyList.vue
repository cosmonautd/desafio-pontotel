<template>
<div id="companies-list">
	<p v-if="companies.length < 1" class="empty-table">
		<!-- Empresas não encontradas -->
	</p>
	<table v-else class="custom-table">
		<tbody>
			<tr v-for="company in companies" :key="company.id">
				<td style="width:60%" class="left-round-corners">{{ company.name }}</td>
				<td>{{ company.symbol }}</td>
				<td class="right-round-corners">
					<button @click="companyDetails(company.id)" class="round-corners">
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
			companies: []
		}
	},
	methods: {
		companyDetails(id) {
			// this.$router.push({ name: 'details', params: {companyId: id}});
			console.log(id)
		},
		get_companies () {
			this.axios.get(`http://localhost:8000/companies`)
			.then((response) => {
				this.companies = response.data.companies
			})
		}
	},
	mounted() {
		this.get_companies()
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