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
              :title="(Object.keys(this.$store.getters.patientsHigh).length + Object.keys(this.$store.getters.patientsMid).length) + ' abnormals'"
              :detail="Object.keys(this.$store.getters.patientsLow).length + ' normals'"
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
  </div>
</template>

<script>
import SummaryCard from '../components/SummaryCard.vue'
export default {
    name: "PatientsPage",
    components:{
        SummaryCard
    }
    
}
</script>

<style>
.info-card{
}
</style>