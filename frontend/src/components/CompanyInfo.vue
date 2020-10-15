<template>
<div id="landing">
	<div class="container-fluid">
		<div class="vertical-spacing-1"></div>
		<div class="vertical-spacing-top"/>
		<h1 class="bovespa-title">{{$route.params.symbol}}</h1>
		<CompanyChart :symbol="$route.params.symbol"/>
		<div class="vertical-spacing-1"></div>
	</div>
</div>
</template>

<script>
import CompanyChart from "./CompanyChart.vue";
export default {
	name: "landing",
	components: {
		CompanyChart
	}
}
</script>

<style scoped>
</style>