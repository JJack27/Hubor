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
          />
        </a-col>
      </a-row>
      <!-- End of header bar-->

      <!-- Start of the patients table -->
      <!-- High Risk Table -->
      <patients-table v-if="Object.keys(this.$store.getters.patientsHigh).length>0"
        title="High Risk"
        :dataSource="this.$store.getters.patientsHighArray"
      />

      <!-- Mid Risk Table -->
      <patients-table v-if="Object.keys(this.$store.getters.patientsMid).length>0"
        title="Midium Risk"
        :dataSource="this.$store.getters.patientsMidArray"
      />

      <!-- Low Risk Table -->
      <patients-table v-if="Object.keys(this.$store.getters.patientsLow).length>0"
        title="Low Risk"
        :dataSource="this.$store.getters.patientsLowArray"
      />
      <!-- End of the patients table -->
  </div>
</template>

<script>
import SummaryCard from '../components/SummaryCard.vue'
import PatientsTable from '../components/PatientsTable.vue'
export default {
    name: "PatientsPage",
    components:{
        SummaryCard,
        PatientsTable,
    }
    
}
</script>

<style>

</style>