<template>
    <div>
        <!-- back arrow -->
        <div style="width:100%; text-align:start">
            <ArrowLeftOutlined @click="backToMonitor" height="2em"/>
        </div>

        <!-- content -->
        <div style="margin-top: 20pt;">
            <a-row type="flex" justify="space-around">
                <a-col class="" :span="8">
                    <PatientContactCardsGroup />
                </a-col>

                <a-col class="" :span="12">
                    <EmergencyContactCardsGroupVertical />
                </a-col>
            </a-row>
        </div>
    </div>
    
</template>

<script>
import PatientContactCardsGroup from '../components/EmergencyContact/PatientContactCardsGroup.vue';
import EmergencyContactCardsGroupVertical from '../components/EmergencyContact/EmergencyContactCardsGroupVertical.vue';
import {ArrowLeftOutlined} from "@ant-design/icons-vue";
export default{
    name:"EmergencyContactPage",
    
    components:{
        ArrowLeftOutlined,
        PatientContactCardsGroup,
        EmergencyContactCardsGroupVertical,
    },

    data(){
        return {
            'id': this.$route.params.id,
        }
    },

    
    mounted(){
        console.log("emergency contact page");
    },

    methods : {
        backToMonitor(){
            this.$router.push("/dashboard/monitor/"+ this.$route.params.id);
        }
    }
}
</script>

<style>

</style>