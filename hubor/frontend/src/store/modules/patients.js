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
    // add given patients to patientsLow, Mid or High based on their status.
    // @param state: vuex component
    // @param patients: a list of patients' object or an object of a single patient
    addPatients: (state, patients) =>{
      // if patients is a list of patients
      if(Array.isArray(patients)){
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
      }else{
        // if patients is an object contain a single patient
        if(patients.status[0] == 0){
          state.patientsLow[patients.id] = patients;
        }else if(patients.status[0] == 1){
          state.patientsMid[patients.id] = patients;
        }else{
          state.patientsHigh[patients.id] = patients;
        }
      }
    },

    // remove givent patients from the state. Notice that the patients parameter contains only the ids
    // @param state: vuex component
    // @param patients: a list of patients' ids or a string of id of a single patient
    removePatients: (state, patients) => {
      if(Array.isArray(patients)){
        // if patients is a list of patients
        for(var i in patients){
          delete state.patientsLow[patients[i]];
          delete state.patientsMid[patients[i]];
          delete state.patientsHigh[patients[i]];
        }
      }else{
        delete state.patientsLow[patients];
        delete state.patientsMid[patients];
        delete state.patientsHigh[patients];
      }
    },
    // end of mutations
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