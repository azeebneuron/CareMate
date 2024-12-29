// src/store/index.js
import { createStore } from 'vuex'
import auth from './modules/auth'
import health from './modules/health'
import tasks from './modules/tasks'
import emergency from './modules/emergency'
import marketplace from './modules/marketplace'
import calls from './modules/calls'

export default createStore({
  modules: {
    auth,
    health,
    tasks,
    emergency,
    marketplace,
    calls
  }
})