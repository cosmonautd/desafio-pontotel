<template>
<div id="app" :class="this.$vssWidth >= 992 ? 'medium-container' : ''">
	<sidebar-menu :menu="menu" :width="'200px'" :collapsed="false" :hideToggle="true" />
	<div class="content">
		<router-view/>
	</div>
</div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import VueScreenSize from 'vue-screen-size'
import { SidebarMenu } from 'vue-sidebar-menu'
import stocks_icon from '@/assets/icons8-stocks-growth-48.png';
import company_icon from '@/assets/icons8-company-48.png';
import about_icon from '@/assets/icons8-about-48.png';
import '@fortawesome/fontawesome-free/css/all.css'
export default {
	name: "App",
	mixins: [VueScreenSize.VueScreenSizeMixin],
	components: {
		SidebarMenu
	},
	data () {
		return {}
	},
	computed: {
		companies_sidebar () {
			if (this.$store.state.companies === null
				|| this.$store.state.companies.length === 0) return [];
			else return this.$store.state.companies.map(company => {
				let obj = {}
				obj.href = `/companies/info/${company.symbol}`;
				obj.title = company.symbol;
				return obj;
			});
		},
		menu () {
			return [
				{
					header: true,
					title: '',
					hiddenOnCollapse: true
				},
				{
					href: '/',
					title: 'Ibovespa',
					icon: {
						element: 'img',
						attributes: { src: stocks_icon },
					}
				},
				{
					href: '/companies',
					title: 'Empresas',
					icon: {
						element: 'img',
						attributes: { src: company_icon },
					},
					child: this.companies_sidebar
				},
				{
					href: '/about',
					title: 'Sobre',
					icon: {
						element: 'img',
						attributes: { src: about_icon },
					}
				}
			]
		}
	},
	methods: {
		get_companies () {
			this.axios.get(`http://localhost:8000/companies`)
			.then((response) => {
				this.$store.commit('update_companies', response.data.companies)
			})
		}
	},
	mounted() {
		this.get_companies()
	}
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

.content {
    padding-left: 150px;
}

.v-sidebar-menu .vsm--link_exact-active, .v-sidebar-menu .vsm--link_active {
	color: #4285f4;
}

.v-sidebar-menu.vsm_expanded .vsm--item_open .vsm--link_level-1 {
	background-color: transparent;
}

.v-sidebar-menu.vsm_expanded .vsm--item_open .vsm--link_level-1 {
	color: #4285f4;
}

.v-sidebar-menu.vsm_expanded .vsm--item_open .vsm--link_level-1 .vsm--icon {
	background-color: transparent;
}
</style>