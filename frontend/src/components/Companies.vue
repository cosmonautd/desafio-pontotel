<template>
<div id="landing">
	<div class="container-fluid">
		<div class="vertical-spacing-1"></div>
		<div class="vertical-spacing-top"/>
		<CompanyList/>
		<div class="vertical-spacing-1"></div>
	</div>
</div>
</template>

<script>
import CompanyList from "./CompanyList.vue";
export default {
	name: "landing",
	components: {
		CompanyList
	}
}
</script>

<style scoped>
</style>