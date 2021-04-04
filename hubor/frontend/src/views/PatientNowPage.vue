<template>
    <div style="margin-top: 20pt;">
        
        <a-row type="flex" justify="space-around">
            <a-col class="current-status-card-cluster" :span="8">
                <PatientNowStatusCard />
            </a-col>

            <a-col class="current-patient-info" :span="12">
                <PatientInfoCard />
            </a-col>
        </a-row>
    </div>
</template>

<script>
import PatientInfoCard from "../components/PatientInfoCard.vue";
import PatientNowStatusCard from "../components/PatientNowStatusCard.vue";

export default{
    name:"PatientNowPage",
    components:{
        PatientNowStatusCard,
        PatientInfoCard,
    },
    
    mounted(){
    }
}
</script>

<style>

</style>