<template>
    <div style="margin-top: 20pt;">
        
        <a-row type="flex" justify="space-around">
            <a-col class="current-status-card-cluster" :span="8">
                <PatientNowStatusCard 
                    @switch-to-history="handleSwitch"
                />
                <br />
                <EmergencyContactButtonCardsGroup />
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
import EmergencyContactButtonCardsGroup from '../components/EmergencyContact/EmergencyContactButtonCardsGroup.vue';

export default{
    name:"PatientNowPage",

    components:{
        PatientNowStatusCard,
        NormalRangeCardsGroup,
        PatientInfoCardsGroup,
        EmergencyContactButtonCardsGroup,
    },

    methods:{
        handleSwitch(vs){
            this.$emit("switch-to-history", vs);
        }
    },
    
    mounted(){

    }
}
</script>

<style>

</style>