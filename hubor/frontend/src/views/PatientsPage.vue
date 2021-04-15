<template>
  <div>
      
      <a-tabs v-model:activeKey="activeKey">
        <a-tab-pane key="1" tab="Abnormal">
          <PatientCardList 
            title="High Risk"
            status="error"
            :dataSource="this.$store.getters.patientsHighArray"
            headerBackColor="#f14062"
            headerFontColor="#ffffff"
            bodyBackColor="#ffffff"
            BodyFontColor="#333333"
            style="width:100%; margin-top:5vh; margin-right: auto; margin-left:auto"
          />
        </a-tab-pane>
        <a-tab-pane key="2" tab="Borderline">
          <PatientCardList
            title="Midium Risk"
            status="warning"
            :dataSource="this.$store.getters.patientsMidArray"
            headerBackColor="#f2bf41"
            headerFontColor="#ffffff"
            bodyBackColor="#ffffff"
            BodyFontColor="#333333"
            style="width:100%; margin-top:5vh; margin-right: auto; margin-left:auto"
          />
        </a-tab-pane>
        <a-tab-pane key="3" tab="Normal">
          <PatientCardList 
            title="Low Risk"
            status="success"
            :dataSource="this.$store.getters.patientsLowArray"
            headerBackColor="#27ce79"
            headerFontColor="#ffffff"
            bodyBackColor="#ffffff"
            BodyFontColor="#333333"
            style="width:100%; margin-top:5vh; margin-right: auto; margin-left:auto"
          />
        </a-tab-pane>

        <a-tab-pane key="4" tab="Pending Requests">
          <PendingRequestCardsGroup />
        </a-tab-pane>
      </a-tabs>

      <a-modal 
        v-model:visible="addPatientModelVisible" 
        title="Add a Patient" 
        :footer="null">
        <AddPatientForm @register-success="handleFormClose"/>
      </a-modal>
  </div>
</template>

<script>
import SummaryCard from '../components/SummaryCard.vue';
import PatientsTable from '../components/PatientsTable.vue';
import PatientListCard from '../components/PatientListCard.vue';
import AddPatientForm from '../components/AddPatientForm.vue';
import PatientCardList from '../components/PatientCardList.vue';
import PendingRequestCardsGroup from '../components/PendingRequests/PendingRequestCardsGroup.vue';
import {ref } from 'vue';

export default {
    name: "PatientsPage",
    components:{
        SummaryCard,
        PatientsTable,
        AddPatientForm,
        PatientListCard,
        PatientCardList,
        PendingRequestCardsGroup,
    },

    mounted(){
      this.activeKey = this.$store.getters.patientPageTabKey;
    },

    

    data(){
      return{
        addPatientModelVisible: false,
        activeKey: this.$store.getters.patientPageTabKey,
      }
    },

    watch:{
      activeKey(val){
        this.$store.dispatch('updatePatientPageTabKey', val);
      }
    },

    methods:{
      showAddPatientModal(){
        this.addPatientModelVisible = true;
      },

      

    }


    
}
</script>

<style>

</style>