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
                    />
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
            dataSource:[]
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