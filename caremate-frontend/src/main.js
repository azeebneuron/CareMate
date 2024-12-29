// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/main.css'  // CORRECTED: Change from './index.css' to './assets/main.css'

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')