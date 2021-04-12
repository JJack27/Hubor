<template>
    <div style="margin-top: 20pt;">
        
        <a-row type="flex" justify="space-around">
            <a-col class="current-status-card-cluster" :span="8">
                <PatientNowStatusCard />
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
import NormalRangeCardsGroup from "../components/NormalRangeCardsGroup.vue";
export default{
    name:"PatientNowPage",
    inject:["id"],

    components:{
        PatientNowStatusCard,
        NormalRangeCardsGroup,
        PatientInfoCardsGroup,
    },
    
    mounted(){
    }
}
</script>

<style>

</style>