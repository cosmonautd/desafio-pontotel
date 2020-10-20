import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

Vue.use(Vuex)

const store = new Vuex.Store({
	state: {
		companies: null
	},
	mutations: {
		update_companies (state, companies) {
			state.companies = companies;
		},
	},
	plugins: [
		createPersistedState({storage: window.sessionStorage})
	]
});

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

import VModal from 'vue-js-modal'
Vue.use(VModal)

Vue.use(VueAxios, axios)

new Vue({
	router,
	store,
	render: h => h(App),
}).$mount('#app')
