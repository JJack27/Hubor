<template>
    <div>
        <div style="margin-top: 20pt;">
            <a-empty v-if="this.havingData == false"/>
            <a-row v-else type="flex" justify="space-around" :gutter="[16,16]">
                <a-col class="vs-history-card-cluster" :span="11">
                    <!-- top row: sort and filter -->
                    <a-row type="flex" justify="space-between">
                        <a-col :span="1" style="text-align:center">
                            <a-button shape="round" type="primary" size="small" style="color: white" @click="changeSortOrder">
                                <i class="fa fa-sort-amount-asc" aria-hidden="true" v-if="this.ascending"/> 
                                <i class="fa fa-sort-amount-desc" aria-hidden="true" v-else/>
                            </a-button>
                        </a-col>
                        <!-- filter icon -->
                        <a-col :span="4" style="text-align:center">
                            <a-popover title="Filter" trigger="click" placement="bottom">
                                <template #content>
                                    <div :style="{ borderBottom: '1px solid #E9E9E9' }">
                                        <a-checkbox
                                            v-model:checked="this.checkAll"
                                            :indeterminate="this.indeterminate"
                                            @change="this.onCheckAllChange"
                                        >
                                            All
                                        </a-checkbox>
                                    </div>
                                    <br />
                                    <a-checkbox-group v-model:value="this.checkedList">
                                        <a-row v-for="item in this.options" :key="item.value">
                                            <a-col :span="24">
                                                <a-checkbox :value="item.value"> {{ item.label }} </a-checkbox>
                                            </a-col>
                                        </a-row>
                                    </a-checkbox-group>
                                </template>
                                <a-button shape="round" type="primary" style="color: white" size="small">
                                    <i class="fa fa-filter" aria-hidden="true" ></i> Filter By
                                </a-button>
                                
                            </a-popover>
                        </a-col>
                    </a-row>
                    <a-divider style="height: 1px; background-color: #c4c1f4; margin-top:5px"></a-divider>
                    <div
                        style="overflow-y:auto; overflow-x:hidden; height:65vh; padding-right:10pt; margin-top:10px"
                    >   
                        <a-timeline v-if="this.dataAbnormal.length != 0">
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
                                    @switch-to-history="handleSwitch"
                                />
                            </a-timeline-item>
                        </a-timeline>
                        <a-empty v-else>
                            <template #description>
                                <span>
                                    No Abnormal Vital Signs
                                </span>
                            </template>
                        </a-empty>
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
            
            // filter variables
            checkAll: true,
            indeterminate: false,
            checkedList: ['hr', 'temp', 'rr', 'spo2'],
            options: [{ label: 'Heart Rate', value: 'hr' },
                      { label: 'Temperature', value: 'temp' },
                      { label: 'Respiration', value: 'rr' },
                      { label: 'Oxygen Saturation', value: 'spo2' },],
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
            if(n != undefined){
                this.reload();
            }
            
        },
        dataSource(n,o){
            this.$forceUpdate();
        },

        dataAbnormal(n,o){
            this.$forceUpdate();
        },

        checkedList(n, o){
            this.indeterminate = !!n.length && n.length < this.options.length;
            this.checkAll = n.length === this.options.length;
            this.reload();
        },
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
        handleSwitch(vs){
            this.vs = vs;
        },

        changeSortOrder(){
            this.ascending = !this.ascending;
            var list = this.dataAbnormal;
            list.reverse(this.ascending);
            this.$forceUpdate();
        },

        reload(){
            this.havingData= true,
            this.$get(`/api/latest1hourvs/${this.$route.params.id}/`)
            .then(response => {
                
                this.dataSource = response.data;
                this.havingData = true;
                // ALTER: requesting all abnormal vital signs
                this.dataAbnormal = response.data.filter((data) => {
                    for(var i in this.checkedList){
                        var vs = this.checkedList[i];
                        var lowerBound = this.$store.getters.patients[this.$route.params.id].normal_range[vs+'_l'];
                        var upperBound = this.$store.getters.patients[this.$route.params.id].normal_range[vs+'_h'];
                        if(parseFloat(data[vs]['mean'].toFixed(1)) < lowerBound || parseFloat(data[vs]['mean'].toFixed(1)) > upperBound){
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
        },

        onCheckAllChange(e){
            this.checkedList = e.target.checked ? this.options.map(item => item.value) : [];
            this.indeterminate =  false;
        },
    }
}
</script>

<style>
.vs-history-card-cluster .ant-timeline-item-tail{
    border-left: 2px solid #c5c4db;
}
</style>