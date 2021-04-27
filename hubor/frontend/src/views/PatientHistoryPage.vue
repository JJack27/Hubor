<template>
    <div>
        <div style="margin-top: 20pt;">
            <a-empty v-if="this.havingData == false"/>
            <a-row v-else type="flex" justify="space-around" :gutter="[16,16]">
                <a-col class="vs-history-card-cluster" :span="11">
                    <!-- top row: sort and filter -->
                    <a-row type="flex" justify="space-between">
                        <a-col :span="1" style="text-align:start">
                            <i class="fa fa-sort-amount-asc" aria-hidden="true" v-if="this.ascending" @click="changeSortOrder"></i>
                            <i class="fa fa-sort-amount-desc" aria-hidden="true" v-else @click="changeSortOrder"></i>
                        </a-col>
                        <a-col :span="1" style="text-align:end">
                            <i class="fa fa-filter" aria-hidden="true"></i>
                        </a-col>
                    </a-row>
                    
                    <div
                        style="overflow-y:auto; overflow-x:hidden; height:65vh; padding-right:10pt;"
                    >   
                        <a-timeline>
                        <a-timeline-item
                            v-for="vs in this.dataAbnormal"
                            :key="vs.time"
                        >
                            <VSHistoryCardGroup
                                :hr="vs.hr.mean"
                                :rr="vs.rr.mean"
                                :spo="vs.spo2.mean"
                                :temp="vs.temp.mean"
                                :bpl="vs.bp_l.mean"
                                :bph="vs.bp_h.mean"
                                :time="vs.time"
                            />
                        </a-timeline-item>
                        </a-timeline>
                    </div>
                </a-col>

                <a-col class="current-patient-info" :span="13">
                    
                    <VSAreaChart 
                        :vsData="this.dataSource"
                        :vs="this.vs"
                        :title="this.title"
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
import VSHistoryCardGroup from '../components/VSHistory/VSHistoryCardGroup.vue';
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
        VSHistoryCardGroup
    },
    data(){
        return {
            dataSource:[],
            dataAbnormal:[],
            vs: this.vsProp,
            stat: "mean",
            title: this.titleProp,
            ascending: true,
            havingData: true,
        }
    },

    watch:{
        vs: function(newVal, oldVal){
            this.title = map[newVal];
        },

        vsProp(newVal, oldVal){
            this.vs = newVal;
        },
        
        '$parent.$parent.$parent.$parent.$parent.activeKey':function(n,o){
            if(n=="2"){
                this.reload();
            }
        },
        
        '$route.params.id':function(n, o){
            this.reload();
        },
        dataSource(n,o){
            this.$forceUpdate();
        },

        dataAbnormal(n,o){
            this.$forceUpdate();
        }
    },

    setup(){
        return {
            //dataSource,
        }
    },

    mounted(){
        this.reload();
    },

    methods:{
        changeSortOrder(){
            this.ascending = !this.ascending;
            var list = this.dataAbnormal;
            list.reverse(this.ascending);
            this.$forceUpdate();
        },

        reload(){
            const validVS = ['hr', 'rr', 'temp', 'spo2']
            this.havingData= true,
            this.$get(`/api/latest1hourvs/${this.$route.params.id}/`)
            .then(response => {
                this.dataSource = response.data;
                this.havingData = true;
                this.dataAbnormal = response.data.filter((data) => {
                    for(var i in validVS){
                        var vs = validVS[i];
                        var lowerBound = this.$store.getters.patients[this.$route.params.id].normal_range[vs+'_l'];
                        var upperBound = this.$store.getters.patients[this.$route.params.id].normal_range[vs+'_h'];
                        if(data[vs]['mean'] <= lowerBound || data[vs]['mean'] >= upperBound){
                            return true;
                        }
                    }
                    return false;
                });
            }).catch(err =>{
                console.log(err)
                this.havingData = false;
            });
            this.$forceUpdate()
        }
    }
}
</script>

<style>
.vs-history-card-cluster .ant-timeline-item-tail{
    border-left: 2px solid #c5c4db;
}
</style>