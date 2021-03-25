// initial state
const state = () => ({
    dashboardKey: ['1'],
    patientPageTabKey: '1',

});
    
// getters
const getters = {
    dashboardKey(state){
        return state.dashboardKey;
    },

    patientPageTabKey(state){
        return state.patientPageTabKey;
    },

}
    
// mutations
const mutations = {

    // update the dashboard selected key. Used for resuming the browsing state
    updateDashboardKey: (state, key) => {
        state.dashboardKey = key;
    },

    updatePatientPageTabKey: (state, key) => {
        state.patientPageTabKey = key;
    },
    // end of mutations
}
  
// actions
const actions = {
    updateDashboardKey: ({commit}, key) => {
      commit('updateDashboardKey', key);
    },

    updatePatientPageTabKey: ({commit}, key) => {
        commit('updatePatientPageTabKey', key);
    },

}
    
  export default {
    namespaced: false,
    state,
    getters,
    actions,
    mutations
  }