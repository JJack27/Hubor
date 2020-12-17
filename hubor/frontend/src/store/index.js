import { createStore } from 'vuex'
import accounts from './modules/accounts'


export default createStore({
  modules:{
    accounts,
  }
})
