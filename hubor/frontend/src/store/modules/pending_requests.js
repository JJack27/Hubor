// initial state
const state = () => ({
    pendingRequests: {}
  });
    
  // getters
  const getters = {
    pendingRequests: (state) => {
      return state.pendingRequests;
    },

    pendingRequestsArray: (state) => {
      var res = [];
      for(var i in state.pendingRequests){
        res.push(state.pendingRequests[i]);
      }
      return res;
    },
  }
    
  // mutations
  const mutations = {
    // add given request to state.PendingRequest.
    // @param state: vuex component
    // @param request: a list of requests object or an object of a single request
    addRequest: (state, request) =>{
      // if request is a list of requests
      if(Array.isArray(request)){
        for (var i in request){
          // add it to the state
          state.pendingRequests[request[i].id] = request[i];
        }
      }else{
        // if it is a single request
        state.pendingRequests[request.id] = request;
      }
    },

    // remove givent request from the state. Notice that the request parameter contains only the ids
    // @param state: vuex component
    // @param request: a list of requests object or an object of a single request
    removeRequest: (state, request) => {
      if(Array.isArray(request)){
        // if request is a list of requests
        for(var i in request){
          delete state.pendingRequests[request[i]];
        }
      }else{
        delete state.pendingRequests[request];
      }
    },
    // end of mutations
  }
  
  // actions
  const actions = {
    addPendingRequests: ({commit}, request) => {
      commit('addRequest', request);
    },
    removePendingRequests: ({commit}, request) => {
      commit('removeRequest', request);
    },
  }
    
  export default {
    namespaced: false,
    state,
    getters,
    actions,
    mutations
  }