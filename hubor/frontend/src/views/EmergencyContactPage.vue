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
                    
                </a-col>

                <a-col class="" :span="12">
                    
                </a-col>
            </a-row>
        </div>
    </div>
    
</template>

<script>
//import PatientContact from '../components/EmergencyContact/PatientContactCardsGroup.vue';
//import EmergencyContactCardsGroupVertical from '../components/EmergencyContact/EmergencyContactCardsGroupVertical.vue';
import {ArrowLeftOutlined} from "@ant-design/icons-vue";
export default{
    name:"EmergencyContactPage",
    
    components:{
        ArrowLeftOutlined,
        //PatientContact,
        //EmergencyContactCardsGroupVertical,
    },

    data(){
        return {
            'id': this.$route.params.id,
        }
    },

    provide(){
        return {
            "id": this.id,
        }
    },
    
    mounted(){
        console.log("emergency contact page");
    },

    methods : {
        backToMonitor(){
            this.$router.push("/dashboard/monitor/"+ this.id);
        }
    }
}
</script>

<style>

</style>