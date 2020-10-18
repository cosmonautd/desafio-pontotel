<template>
<div id="landing">
	<div class="container-fluid">
		<div class="vertical-spacing-1"></div>
		<div class="vertical-spacing-top"/>
		<h1 class="bovespa-title">{{$route.params.symbol}}</h1>
		<Chart :symbol="$route.params.symbol"/>
		<div class="vertical-spacing-1"></div>
	</div>
</div>
</template>

<script>
import Chart from "./Chart.vue";
export default {
	name: "landing",
	components: {
		Chart
	}
}
</script>

<style scoped>
</style>