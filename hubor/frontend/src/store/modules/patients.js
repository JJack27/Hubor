// initial state
const state = () => ({
    patients: {},

  });
    
  // getters
  const getters = {
    patients: (state) => {
      return state.patients;
    },
  
  
  }
    
  // mutations
  const mutations = {
  }
  
  // actions
  const actions = {
  }
    
  export default {
    namespaced: false,
    state,
    getters,
    actions,
    mutations
  }