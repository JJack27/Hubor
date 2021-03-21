<template>
    <div>
        <PatientListCard
            title="Low Risk"
            :dataSource="this.$store.getters.patientsLowArray"
            headerBackColor="#27ce79"
            headerFontColor="#ffffff"
            bodyBackColor="#ffffff"
            BodyFontColor="#333333"
            style="width:80%"
        />
    </div>

</template>

<style>

</style>

<script>
import PatientListCard from "../components/PatientListCard.vue";
export default {
  name: "Home", 
  components: {
      PatientListCard,
  },

  mounted(){
    console.log(this.$store.getters.patientsLow);
  }
};
</script>