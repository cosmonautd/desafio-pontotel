<template>
<div id="landing">
	<div class="container-fluid">
		<div class="vertical-spacing-1"></div>
		<div class="vertical-spacing-top"/>
		<h1 class="bovespa-title">bovespa</h1>
		<Chart :symbol="'BOVB11.SAO'"/>
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