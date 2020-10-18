<template>
<div id="app" :class="this.$vssWidth >= 992 ? 'medium-container' : ''">
	<router-view/>
	<sidebar-menu :menu="menu" :collapsed="true" :hideToggle="true" />
</div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import VueScreenSize from 'vue-screen-size'
import { SidebarMenu } from 'vue-sidebar-menu'
export default {
	name: "App",
	mixins: [VueScreenSize.VueScreenSizeMixin],
	components: {
		SidebarMenu
	},
	data () {
		return {
			menu: [
				{
					header: true,
					title: 'Main Navigation',
					hiddenOnCollapse: true
				},
				{
					href: '/',
					title: 'Bovespa',
					icon: 'fa fa-user'
				},
				{
					href: '/companies',
					title: 'Empresas',
					icon: 'fa fa-user'
				},
				{
					href: '/about',
					title: 'Sobre',
					icon: 'fa fa-chart-area'
				}
			]
		}
	},
}
</script>

<style lang="scss">
h1 {
	color: #01a2b5
}
body {
	color: #222;
	background-color: #efeff1;
}
p {
	margin-bottom: 0%;
}
.spacing-top {
	margin-top: 1.5em;
}
#app {
	margin-top: 1em;
	display: block;
	text-align: center;
	font-family: Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}
.align-left {
	text-align: left;
}
.bovespa-title {
	font-weight: bold;
}
.center {
  margin: auto;
  width: 50%;
}
.medium-container {
	max-width: 1400px;
}
.bovespa-modal {
	background-color: #1D1D1D;
	width: 100%;
	height: 100%;
}
.bv-example-row {
	height: 100%;
}
.round-corners {
	border-radius: 15px 15px 15px 15px;
}
.vertical-spacing-1 {
	height: 1em;
}
.vertical-spacing-2 {
	height: 2em;
}
.vertical-spacing-3 {
	height: 3em;
}
.vertical-spacing-4 {
	height: 4em;
}
.vertical-spacing-8 {
	height: 8em;
}
.unselectable a, p, h1, div {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.button, a.button, button, [type=submit], [type=reset], [type=button] {
	margin: 0 0.5em 0 0;
	width: 8em;
	background-color: #f66250;
	border-color: #f66250;
}

.button:hover, a.button:hover, button:hover, [type=submit]:hover, [type=reset]:hover, [type=button]:hover {
	background-color: #d05236;
	border-color: #d05236;
}

.button:focus, .button:active, a.button:focus, a.button:active, button:focus, button:active, [type=submit]:focus, [type=submit]:active, [type=reset]:focus, [type=reset]:active, [type=button]:focus, [type=button]:active {
	background-color: #d05236;
	border-color: #d05236;
  }

/* Make scroll bars invisible */

html {
    scrollbar-width: none; /* For Firefox */
    -ms-overflow-style: none; /* For Internet Explorer and Edge */
}

html::-webkit-scrollbar {
    width: 0px; /* For Chrome, Safari, and Opera */
}
</style>