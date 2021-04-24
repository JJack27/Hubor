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
                        :vs="this.vsProp"
                        :title="this.titleProp"
                        stat="mean"
                    />
                    <br/>
                    <!-- button group - vs -->
                    <a-radio-group v-model:value="vs" button-style="solid">
                        <a-radio-button value="hr">HR</a-radio-button>
                        <a-radio-button value="temp">TEMP</a-radio-button>
                        <a-radio-button value="rr">RR</a-radio-button>
                        <a-radio-button value="spo2">SPO2</a-radio-button>
                    </a-radio-group>
                    
                </a-col>
            </a-row>
        </div>
        
    </div>
</template>
  
<script>
import VSAreaChart from '../components/ChartsPlots/VSAreaChart.vue';
import {provide, ref, reactive, inject} from 'vue';
const map={
    "hr": "heart rate",
    "rr": "respiration rate",
    "spo2": `O${"2".sub()} Saturation`,
    "temp": "temperature"
}
export default{
    name:"PatientHistoryPage",
    inject:['id'],
    props:['vsProp', 'titleProp'],
    components:{
        VSAreaChart,
    },
    data(){
        return {
            dataSource:[],
            vs: this.vsProp,
            stat: "mean",
            title: this.titleProp
        }
    },

    watch:{
        vs: function(newVal, oldVal){
            this.title = map[newVal];
        },

        vsProp(newVal, oldVal){
            this.vs = newVal;
        }
    },

    setup(){
        return {
            //dataSource,
        }
    },

    mounted(){
        console.log(this.vsProp);
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