import Vue from 'vue'
import Router from 'vue-router'

import Landing from './components/Landing.vue'
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
