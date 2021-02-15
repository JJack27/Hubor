// initial state
const state = () => ({
    patientsLow: {},
    patientsHigh: {},
    patientsMid: {}
  });
    
  // getters
  const getters = {
    patients: (state) => {
      var ans = Object.assign({}, state.patientsLow, state.patientsMid, state.patientsHigh);
      return ans;
    },

    patientsLow: (state) => {
      return state.patientsLow;
    },

    patientsMid: (state) => {
      return state.patientsMid;
    },

    patientsHigh: (state) => {
      return state.patientsHigh;
    }
   
  
  }
    
  // mutations
  const mutations = {
    addPatients: (state, patients) =>{
      console.log(patients);
      for (var i in patients){
        // check status and orgnize it
        if(patients[i].status[0] == 0){
          state.patientsLow[patients[i].id] = patients[i];
          
        }else if(patients[i].status[0] == 1){
          state.patientsMid[patients[i].id] = patients[i];
        }else{
          state.patientsHigh[patients[i].id] = patients[i];
        }
      }
    },
  }
  
  // actions
  const actions = {
    addPatients: ({commit, state}, patients) => {
      commit('addPatients', patients);
    },
  }
    
  export default {
    namespaced: false,
    state,
    getters,
    actions,
    mutations
  }