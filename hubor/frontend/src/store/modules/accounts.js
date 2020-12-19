// initial state
// shape: [{ id, quantity }]
const state = () => ({
  id:"",
  firstName: "",
  lastName: "",
  userType:1,
  since: "",
  phone: "",
  email: "",
  dateOfBirth: ""
});
  
// getters
const getters = {
  currentUserInfo: (state) => {
    return state;
  },


}
  
// mutations
const mutations = {
  updateInfo: (state, userInfo) =>{
    state.id = userInfo.id;
    state.firstName = userInfo.first_name;
    state.lastName = userInfo.last_name;
    state.userType = userInfo.user_type;
    state.since = userInfo.date_joined;
    state.phone = userInfo.phone;
    state.email = userInfo.email;
    state.dateOfBirth = userInfo.date_of_birth
  },

  clearInfo: (state) => {
    state.id = "",
    state.firstName = "",
    state.lastName = "",
    state.userType = 1,
    state.since = "",
    state.phone = "",
    state.email = "",
    state.dateOfBirth = ""
  }
  
}

// actions
const actions = {
  login : ({commit, state}, userInfo) => {
    commit('updateInfo', userInfo);
  },

  logout : ({commit, state}) => {
    commit('clearInfo');
  }

}
  
export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}