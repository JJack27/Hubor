<template>
    <div style="margin-top: 20pt;">
        
        <a-row type="flex" justify="space-around">
            <a-col class="current-status-card-cluster" :span="8">
                <PatientNowStatusCard />
                <br />
                <EmergencyContactCardsGroup 
                    :dataSource=this.$store.getters.patients[this.id].emergency_contacts
                />
            </a-col>

            <a-col class="current-patient-info" :span="12">
                <PatientInfoCardsGroup />
                <br />
                <NormalRangeCardsGroup style=""/>
            </a-col>
        </a-row>
    </div>
</template>

<script>
//import PatientInfoCard from "../components/PatientInfoCard.vue";
import PatientInfoCardsGroup from "../components/PatientInfoCardsGroup.vue";
import PatientNowStatusCard from "../components/PatientNowStatusCard.vue";
import NormalRangeCardsGroup from "../components/NormalRange/NormalRangeCardsGroup.vue";
import EmergencyContactCardsGroup from '../components/EmergencyContact/EmergencyContactCardsGroup.vue';

export default{
    name:"PatientNowPage",
    inject:["id"],

    components:{
        PatientNowStatusCard,
        NormalRangeCardsGroup,
        PatientInfoCardsGroup,
        EmergencyContactCardsGroup,
    },
    
    mounted(){
    }
}
</script>

<style>

</style>