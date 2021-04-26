<template>
    <div class="emergency-contact-card-wrapper">
        <h1 style="font-weight: bold; text-align: start;">
            Emergency Contact
        </h1>
        <a-row  type="flex" justify="bottom" :gutter="[16,16]">

            <!-- button card redirects to /dashboard/emergencycontacts/id -->
            <a-col
                :span="8"
                style="height: 180px !important;"
            >
                <PatientButtonCard 
                    style="height:100% !important;"
                />
            </a-col>

            <!-- button card redirects to /dashboard/emergencycontacts/id -->
            <a-col
                :span="8"
                style="height: 180px !important;"
            >
                <EMButtonCard 
                    style="height:100% !important;"
                />
            </a-col>
            
            <!-- card button for adding new emergency contact -->
            <a-col
                :span="8"
                style="height: 180px !important;"
            >
                <AddEMButtonCard 
                    style="height:100% !important;"
                />
            </a-col>
        </a-row>
        
        
        
    </div>
</template>

<script>
import AddEMButtonCard from './ButtonCard/AddEMButtonCard.vue';
import PatientButtonCard from './ButtonCard/PatientButtonCard.vue';
import EMButtonCard from './ButtonCard/EMButtonCard.vue';


export default{
    name: "EmergencyButtonContactCardsGroup",
    components:{
        AddEMButtonCard,
        PatientButtonCard,
        EMButtonCard,
    },
    data(){
        return{
            id: this.$route.params.id,
        }
    },

}
</script>

<style>
.emergency-contact-wrapper-card .ant-card{
    border-radius: 10px !important;
}
</style>