import Vue from 'vue'
import Router from 'vue-router'

import Landing from './components/Landing.vue'
import Companies from './components/Companies.vue'
import CompanyInfo from './components/CompanyInfo.vue'
import About from './components/About.vue'

Vue.use(Router)

export default new Router({
	routes: [
		{
			path: '/',
			name: 'landing',
			component: Landing
		},
		{
			path: '/companies',
			name: 'companies',
			component: Companies
		},
		{
			path: '/companies/info/:symbol',
			name: 'company_info',
			component: CompanyInfo
		},
		{
			path: '/about',
			name: 'about',
			component: About
		}
	],
	scrollBehavior: (to, from, savedPosition) => {
		if (savedPosition) {
			return savedPosition;
		} else if (to.hash) {
			return {
			selector: to.hash
			};
		} else {
			return { x: 0, y: 0 };
		}
	}
});
