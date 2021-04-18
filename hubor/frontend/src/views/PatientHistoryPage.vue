<template>
    <div>
        <div style="margin-top: 20pt;">
        
            <a-row type="flex" justify="space-around">
                <a-col class="current-status-card-cluster" :span="8">
                    <a-button @click="update">Update</a-button>
                </a-col>

                <a-col class="current-patient-info" :span="12">
                    
                    <VSAreaChart 
                        :vsData="this.dataSource"
                        :vs="this.vs"
                        :stat="this.stat"
                    />
                    <br/>
                    <!-- button group - vs -->
                    <a-radio-group v-model:value="vs" button-style="solid">
                        <a-radio-button value="hr">HR</a-radio-button>
                        <a-radio-button value="temp">TEMP</a-radio-button>
                        <a-radio-button value="rr">RR</a-radio-button>
                        <a-radio-button value="spo2">SPO2</a-radio-button>
                    </a-radio-group>
                    <br/>
                    <!-- button group - stat -->
                    <a-radio-group v-model:value="stat" button-style="solid" style="margin-top:10pt">
                        <a-radio-button value="mean">Mean</a-radio-button>
                        <a-radio-button value="med">Median</a-radio-button>
                        <a-radio-button value="min">Min</a-radio-button>
                        <a-radio-button value="max">Max</a-radio-button>
                        <a-radio-button value="std">Variance</a-radio-button>
                    </a-radio-group>
                </a-col>
            </a-row>
        </div>
        
    </div>
</template>
  
<script>
import VSAreaChart from '../components/ChartsPlots/VSAreaChart.vue';
import {provide, ref, reactive, inject} from 'vue';
export default{
    name:"PatientHistoryPage",
    inject:['id'],

    components:{
        VSAreaChart,
    },
    data(){
        return {
            dataSource:[],
            vs: "hr",
            stat: "mean",
        }
    },

    setup(){
        return {
            //dataSource,
        }
    },

    mounted(){
        this.$get(`/api/latest1hourvs/${this.id}/`)
            .then(response => {
                this.dataSource = response.data;
            });
    },

    methods:{
        update(){
            this.$get(`/api/latest1hourvs/${this.id}/`)
                .then(response => {
                    this.dataSource = response.data;
                    
                });
            console.log(this.dataSource);
        }
    }
}
</script>

<style>

</style>