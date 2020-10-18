<template>
<div id="landing">
	<div class="vertical-spacing-1"></div>
	<div class="vertical-spacing-top"/>
	<b-container fluid class="bv-example-row">
		<b-row align-h="center" style="height: 100%;">
			<b-col xs="10" sm="10" md="10" lg="10" xl="10" align-self="center">
				<b-row align-h="center" align-v="start">
					<h1 class="bovespa-title" style="color: #444">Ibovespa</h1>
				</b-row>
			</b-col>
			<b-col sm="12" md="12" lg="12" xl="12">
				<Chart :symbol="'BOVB11.SAO'"/>
			</b-col>
		</b-row>
	</b-container>
</div>
</template>

<script>
import Chart from "./Chart.vue";
import VueScreenSize from 'vue-screen-size'
export default {
	name: "landing",
	components: {
		Chart
	},
	mixins: [VueScreenSize.VueScreenSizeMixin],
}
</script>

<style scoped>
.bv-example-row {
	height: 100%;
}
</style>