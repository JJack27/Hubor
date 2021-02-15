import { createStore } from 'vuex'
import accounts from './modules/accounts'
import patients from './modules/patients'

export default createStore({
  modules:{
    accounts,
    patients,
  }
})
