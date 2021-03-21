<template>
  <div>
      <!-- Top cards bar -->
      <a-row type="flex" justify="space-around"> 
        <!-- Basic card -->
        <a-col class="info-card" :span="6">
          <summary-card
            headerImage="home/banner/home-greeting.jpg"
            avatar="home/avatar/flag.png"
            :title="'Hi, Dr. ' + this.$store.getters.currentUserInfo.lastName"
            :detail="'since: ' + (new Date(this.$store.getters.currentUserInfo.since)).toDateString()"
          />  
        </a-col>

        <!-- Patients summary -->
        <a-col class="info-card" :span="6">
          <summary-card
              headerImage="home/banner/home-patients.jpg"
              avatar="home/avatar/doctor-logo.jpg"
              :title="(Object.keys(this.$store.getters.patientsHigh).length + Object.keys(this.$store.getters.patientsMid).length) + ' abnormal(s)'"
              :detail="Object.keys(this.$store.getters.patientsLow).length + ' normal(s)'"
          />
        </a-col>

        <!-- Add a patient -->
        <a-col class="info-card" :span="6">
          <summary-card
              headerImage="home/banner/home-new-patient.jpg"
              avatar="home/avatar/add-patient.jpg"
              title="Add a Patient"
              detail="to your facility"
              @click="showAddPatientModal"
          />
        </a-col>
      </a-row>
      <!-- End of header bar-->

      <!-- Start of the patients table -->
      <!-- High Risk Table -->
      <PatientListCard v-if="Object.keys(this.$store.getters.patientsHigh).length>0"
        title="High Risk"
        :dataSource="this.$store.getters.patientsHighArray"
        headerBackColor="#f14062"
        headerFontColor="#ffffff"
        bodyBackColor="#ffffff"
        BodyFontColor="#333333"
        style="width:92%; margin-top:5vh; margin-right: auto; margin-left:auto"
      />

      <!-- Mid Risk Table -->
      <PatientListCard v-if="Object.keys(this.$store.getters.patientsMid).length>0"
        title="Midium Risk"
        :dataSource="this.$store.getters.patientsMidArray"
        headerBackColor="#f2bf41"
        headerFontColor="#ffffff"
        bodyBackColor="#ffffff"
        BodyFontColor="#333333"
        style="width:92%; margin-top:5vh; margin-right: auto; margin-left:auto"
      />

      <!-- Low Risk Table -->
      <PatientListCard v-if="Object.keys(this.$store.getters.patientsLow).length>0"
        title="Low Risk"
        :dataSource="this.$store.getters.patientsLowArray"
        headerBackColor="#27ce79"
        headerFontColor="#ffffff"
        bodyBackColor="#ffffff"
        BodyFontColor="#333333"
        style="width:92%; margin-top:5vh; margin-right: auto; margin-left:auto"
      />
      <!-- End of the patients table -->

      <!--
      <patients-table v-if="Object.keys(this.$store.getters.patientsHigh).length>0"
        title="High Risk"
        :dataSource="this.$store.getters.patientsHighArray"
      />

      <patients-table v-if="Object.keys(this.$store.getters.patientsMid).length>0"
        title="Midium Risk"
        :dataSource="this.$store.getters.patientsMidArray"
      />

      <patients-table v-if="Object.keys(this.$store.getters.patientsLow).length>0"
        title="Low Risk"
        :dataSource="this.$store.getters.patientsLowArray"
      />
      -->


      <a-modal 
        v-model:visible="addPatientModelVisible" 
        title="Add a Patient" 
        :footer="null">
        <AddPatientForm @register-success="handleFormClose"/>
      </a-modal>
  </div>
</template>

<script>
import SummaryCard from '../components/SummaryCard.vue'
import PatientsTable from '../components/PatientsTable.vue'
import PatientListCard from '../components/PatientListCard.vue'
import AddPatientForm from '../components/AddPatientForm.vue'
export default {
    name: "PatientsPage",
    components:{
        SummaryCard,
        PatientsTable,
        AddPatientForm,
        PatientListCard
    },

    data(){
      return{
        addPatientModelVisible: false,
      }
    },

    methods:{
      showAddPatientModal(){
        this.addPatientModelVisible = true;
      },

      handleFormClose(patientId){
        // add patient to doctor's facility
        this.$put('api/belongsto/'+this.$store.getters.currentUserInfo.facility.id+'/', {"user": patientId})
          .then((response) => {
            //console.log('belongsto', response);
            // assign doctors to the patient
            this.$post('api/takecareof/'+this.$store.getters.userId+"/"+patientId +"/", {})
              .then((response) => {
                // update front end page
                this.$get('api/patientsof/'+this.$store.getters.userId + '/')
                .then((response) =>{
                  this.$store.dispatch('addPatients', response.data);
                });
            });
        });
        this.addPatientModelVisible = false;
      },

    }


    
}
</script>

<style>

</style>