<template>
    <div style="margin-top: 20pt;">
        <h1 style="font-weight: bold">
            {{ this.$store.getters.patients[this.id].first_name +
            " " + this.$store.getters.patients[this.id].last_name}}
        </h1>
        <a-row type="flex" justify="space-around">
            <a-col class="current-status-card-cluster" :span="8">
                <PatientNowStatusCard />
            </a-col>

            <a-col class="current-patient-info" :span="12">
                <PatientInfoCardsGroup />
            </a-col>
        </a-row>
    </div>
</template>

<script>
import PatientInfoCard from "../components/PatientInfoCard.vue";
import PatientInfoCardsGroup from "../components/PatientInfoCardsGroup.vue";
import PatientNowStatusCard from "../components/PatientNowStatusCard.vue";

export default{
    name:"PatientNowPage",
    inject:["id"],

    components:{
        PatientNowStatusCard,
        PatientInfoCard,
        PatientInfoCardsGroup,
    },
    
    mounted(){
    }
}
</script>

<style>

</style>