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
    },

    patientsLowArray: (state) => {
      var res = [];
      for(var i in state.patientsLow){
        res.push(state.patientsLow[i]);
      }
      return res;
    },

    patientsMidArray: (state) => {
      var res = [];
      for(var i in state.patientsMid){
        res.push(state.patientsMid[i]);
      }
      return res;
    },

    patientsHighArray: (state) => {
      var res = [];
      for(var i in state.patientsHigh){
        res.push(state.patientsHigh[i]);
      }
      return res;
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

    // append an emergency contact to a given user
    appendEmergencyContact(state, emergencyContact){
      if(emergencyContact.patient in state.patientsLow){
        state.patientsLow[emergencyContact.patient].emergency_contacts.push(emergencyContact);
      }else if(emergencyContact.patient in state.patientsMid){
        state.patientsMid[emergencyContact.patient].emergency_contacts.push(emergencyContact);
      }else{
        state.patientsHigh[emergencyContact.patient].emergency_contacts.push(emergencyContact);
        console.log(state.patientsHigh[emergencyContact.patient].emergency_contacts)
        console.log(emergencyContact);
      }
    }
    // end of mutations
  }
  
  // actions
  const actions = {
    addPatients: ({commit}, patients) => {
      commit('addPatients', patients);
    },

    appendEmergencyContact({commit}, emergencyContact){
      commit('appendEmergencyContact', emergencyContact);
    }
  }
    
  export default {
    namespaced: false,
    state,
    getters,
    actions,
    mutations
  }