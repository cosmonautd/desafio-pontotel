<template>
<div id="landing">
	<div class="container-fluid">
		<div class="vertical-spacing-1"></div>
		<div class="vertical-spacing-top"/>
		<h1 class="bovespa-title">bovespa</h1>
		<BovespaChart/>
		<div class="vertical-spacing-2"></div>
		<h1 class="bovespa-title">empresas</h1>
		<div v-if="companies.length > 0">
			<CompanyList
				:companies="companies"
			/>
		</div>
		<button class="round-corners" @click="about">
			sobre
		</button>
		<div class="vertical-spacing-1"></div>
	</div>
</div>
</template>

<script>
import BovespaChart from "./BovespaChart.vue";
import CompanyList from "./CompanyList.vue";
export default {
	name: "landing",
	components: {
		BovespaChart,
		CompanyList
	},
	data() {
		return {
			companies: [
				{
					id: 1,
					name: 'Ambev',
					ticker: 'ABEV'
				}
			]
		}
	},
	methods: {
		about() {
			this.$router.push({ name: 'about'});
		}
	}
}
</script>

<style scoped>
.footer {
	color: #FFF;
	background-color: #222;
	margin: 0.25em 0.5em 0.25em 0.5em;
	display: inline-block;
	padding: 1.25em 2em 1.25em 2em;
	cursor: pointer;
	display: inline-block;
}
</style>