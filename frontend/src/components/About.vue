<template>
<div id="about" class="small-container">
	<div class="container-fluid">
		<div class="vertical-spacing-1"></div>
		<div class="vertical-spacing-top"/>
		<div @click="landingPage" class="link">
			<h1 class="bovespa-title" style="color: #444">
				Ibovespa/Empresas
			</h1>
		</div>
		<p>
			Acompanhe o Índice Bovespa e as 10 maiores empresas do Brasil em tempo real
		</p>
		<div class="vertical-spacing-2"/>
		<div class="content">
			<p>
				<!-- Este projeto faz parte do desafio do processo de seleção da PontoTel.  -->
			</p>
		</div>
	</div>
	<div class="vertical-spacing-3"/>
</div>
</template>

<script>
export default {
	name: "about",
	methods: {
		landingPage() {
			this.$router.push({name: 'landing'});
		}
	}
}
</script>

<style scoped>
.link {
	text-decoration: none;
	cursor: pointer;
}
.content {
	text-align: justify;
}
.bold {
	font-weight: bold;
}
.card {
	color: #FFF;
	background-color: #222;
	margin: 0.25em 0.25em 0.25em 0.25em;
	display: inline-block;
	padding: 1em 1.5em 1em 1.5em;
	cursor: pointer;
	display: inline-block;
}
.white {
	color: #FFF
}
</style>