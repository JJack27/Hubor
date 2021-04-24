<template>
    <div class="patient-info-cards-group">
        
        <h1 style="font-weight: bold; text-align: start;">
            Customize Normal Range
        </h1>

        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <!-- HR -->
            <a-col :span="8">
                <NormalRangeCard
                    icon="hr_icon.png"
                    :low="this.ranges.hr_l"
                    :high="this.ranges.hr_h"
                    unit="bpm"
                    title="Heart Rate"
                    prefix="hr"
                    @save-normal-range="updateNormalRange"
                />
            </a-col>

            <!-- TEMP -->
            <a-col :span="8">
                <NormalRangeCard
                    icon="temp_icon.png"
                    :low="this.ranges.temp_l"
                    :high="this.ranges.temp_h"
                    unit="°C"
                    title="Temperature"
                    prefix="temp"
                    @save-normal-range="updateNormalRange"
                />
            </a-col>

            <!-- SPO2 -->
            <a-col :span="8">
                <NormalRangeCard
                    icon="spo2_icon.png"
                    :low="this.ranges.spo2_l"
                    :high="this.ranges.spo2_h"
                    unit="%"
                    title="O<sub>2</sub> Saturation"
                    prefix="spo2"
                    @save-normal-range="updateNormalRange"
                />
            </a-col>
        </a-row>

        
        <a-row type="flex" justify="bottom" :gutter="[16,16]">

            <!-- RR -->
            <a-col :span="8">
                <NormalRangeCard
                    icon="rr_icon.png"
                    :low="this.ranges.rr_l"
                    :high="this.ranges.rr_h"
                    unit="rpm"
                    title="Respiration Rate"
                    prefix="rr"
                    @save-normal-range="updateNormalRange"
                />
            </a-col>

            <!-- BP -->
            <a-col :span="16">
                <NormalRangeCard
                    icon="bp_icon.png"
                    :low="this.ranges.bp_l"
                    :high="this.ranges.bp_h"
                    unit="mmHg"
                    title="Blood Pressure"
                    prefix="bp"
                    @save-normal-range="updateNormalRange"
                />
            </a-col>
        </a-row>
    </div>

</template>

<script>
import NormalRangeCard from './NormalRangeCard.vue';
export default{
    name: "NormalRangeCardsGroup",
    
    inject: [
        'id'
    ],

    provide(){
        return {
            'ranges': this.ranges,
        }
    },

    components:{
        NormalRangeCard
    },

    data(){
        return {
            normalRangeVisiable: false,
            ranges: this.$store.getters.patients[this.id].normal_range,
        }
    },

    methods:{
        /*
        handleFormOpen(){
            this.normalRangeVisiable = true;
        },

        handleFormClose(rawState){
            // this.ranges = rawState;
            this.normalRangeVisiable = false;
        },
        */

        updateNormalRange(state){
            for(var i in state){
                console.log(i);
                console.log(this.ranges[i]);
                this.ranges[i] = state[i];
            }
        }
    },

    setup() {
        
    },

}

</script>

<style>
.patient-info-cards-group .ant-card-bordered{
    border-radius: 10px !important;
    text-align: start !important;
}
</style>