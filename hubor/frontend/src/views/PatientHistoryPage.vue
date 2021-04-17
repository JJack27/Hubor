<template>
    <div>
        <div style="margin-top: 20pt;">
        
            <a-row type="flex" justify="space-around">
                <a-col class="current-status-card-cluster" :span="8">
                </a-col>

                <a-col class="current-patient-info" :span="12">
                    <VSAreaChart />
                </a-col>
            </a-row>
        </div>
        
    </div>
</template>
  
<script>
import VSAreaChart from '../components/ChartsPlots/VSAreaChart.vue';

export default{
    name:"PatientHistoryPage",
    inject:['id', ],

    components:{
        VSAreaChart,
    },

    setup(){

    },

    mounted(){
        console.log(this.id);
    }
}
</script>

<style>

</style>