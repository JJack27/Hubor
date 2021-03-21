// initial state
const state = () => ({
    patientsLow: {
      
      "589b13c6-a719-4a20-9928-825bbc1d48c7": {
          "id": "589b13c6-a719-4a20-9928-825bbc1d48c7",
          "first_name": "Yizhou",
          "last_name": "Zhao",
          "email": "example@exa.com",
          "user_type": 0,
          "height": 175,
          "weight": 63,
          "date_of_birth": "2010-01-01",
          "notes": "123123",
          "phone": "7806312714",
          "status": [
            0
          ],
          "facility": {
            "id": "ebe49003-dbc9-4e1f-938a-8359ddf58745",
            "name": "facility",
            "address": "123123123",
            "phone": "123123123",
            "description": null
          },
          "hr": "68",
          "temp": "36.5",
          "rr": "40",
          "spo2": "94"
        },

        
        "82a81853-4f37-4617-8017-79a52cc28e8c": {
            "id": "82a81853-4f37-4617-8017-79a52cc28e8c",
            "first_name": "Jack",
            "last_name": "Lee",
            "email": "example@exa.ple",
            "user_type": 0,
            "height": 178,
            "weight": 85,
            "date_of_birth": "2010-01-01",
            "notes": "123123",
            "phone": "1238598492",
            "status": [
              0
            ],
            "facility": {
              "id": "ebe49003-dbc9-4e1f-938a-8359ddf58745",
              "name": "facility",
              "address": "123123123",
              "phone": "123123123",
              "description": null
            },
            "hr": "90",
            "temp": "34.8",
            "rr": "37",
            "spo2": "99"
          }
        
      
    },
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