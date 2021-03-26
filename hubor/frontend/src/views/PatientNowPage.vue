<template>
    <div style="margin-top: 20pt;">
        
        <a-row type="flex" justify="space-around">
            <a-col class="current-status-card-cluster" :span="8">
                <PatientNowStatusCard
                    :id="this.id"
                />
            </a-col>

            <a-col class="current-patient-info" :span="12">
                <PatientInfoCard 
                    :id="this.id"
                />
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
    data(){
        return {
            "id" : this.$route.params.id,
        }
    },
    mounted(){
        
    }
}
</script>

<style>

</style>