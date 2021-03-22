import { createStore } from 'vuex'
import accounts from './modules/accounts'
import patients from './modules/patients'
import pending_requests from './modules/pending_requests';

export default createStore({
  modules:{
    accounts,
    patients,
    pending_requests,
  }
})
