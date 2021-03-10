// initial state
const state = () => ({
  currentUser:{
    id:"",
    firstName: "",
    lastName: "",
    userType:1,
    since: "",
    phone: "",
    email: "",
    dateOfBirth: "",
    facility:""
  }

  
});
  
// getters
const getters = {
  currentUserInfo: (state) => {
    return state.currentUser;
  },

  userId :(state) => {
    return state.currentUser.id;
  }


}
  
// mutations
const mutations = {
  updateInfo: (state, userInfo) =>{
    state.currentUser.id = userInfo.id;
    state.currentUser.firstName = userInfo.first_name;
    state.currentUser.lastName = userInfo.last_name;
    state.currentUser.userType = userInfo.user_type;
    state.currentUser.since = userInfo.date_joined;
    state.currentUser.phone = userInfo.phone;
    state.currentUser.email = userInfo.email;
    state.currentUser.dateOfBirth = userInfo.date_of_birth;
    state.currentUser.facility = userInfo.facility;
  },

  clearInfo: (state) => {
    state.currentUser.id = "",
    state.currentUser.firstName = "",
    state.currentUser.lastName = "",
    state.currentUser.userType = 1,
    state.currentUser.since = "",
    state.currentUser.phone = "",
    state.currentUser.email = "",
    state.currentUser.dateOfBirth = ""
    state.currentUser.facility = ""
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
  namespaced: false,
  state,
  getters,
  actions,
  mutations
}