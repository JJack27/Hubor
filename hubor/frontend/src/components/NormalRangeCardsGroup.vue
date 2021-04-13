<template>
    <div class="patient-info-cards-group">
        
        <h1 style="font-weight: bold; text-align: start;">
            Normal Range
        </h1>

        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <!-- HR -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="hr_icon.png"
                    :value="this.ranges.hr_h + '/' + this.ranges.hr_l"
                    unit="bpm"
                    title="Heart Rate"
                />
            </a-col>

            <!-- TEMP -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="temp_icon.png"
                    :value="this.ranges.temp_h + '/' + this.ranges.temp_l"
                    unit="°C"
                    title="Temperature"
                />
            </a-col>

            <!-- SPO2 -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="spo2_icon.png"
                    :value="this.ranges.spo2_h + '/' + this.ranges.spo2_l"
                    unit="%"
                    title="Oxygen Saturation"
                />
            </a-col>
        </a-row>

        
        <a-row type="flex" justify="bottom" :gutter="[16,16]">

            <!-- RR -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="this.ranges.rr_h + '/' + this.ranges.rr_l"
                    unit="rpm"
                    title="Respiration Rate"
                />
            </a-col>

            <!-- BP -->
            <a-col :span="16">
                <VSEntryHorizontal
                    icon="bp_icon.png"
                    :value="this.ranges.bp_h + '/' + this.ranges.bp_l"
                    unit="mmHg"
                    title="Blood Pressure"
                />
            </a-col>
        </a-row>
        <br/>
        <div style="text-align:end;">
            <a-button 
                @click="handleFormOpen"
                type="primary"
            >
                Edit Normal Ranges
            </a-button>
        </div>

        <a-modal 
            v-model:visible="normalRangeVisiable" 
            title="Edit Normal Ranges" 
            :footer="null"
            :closable="false"
        >
            <NormalRangesForm 
                @edited-normal-ranges="handleFormClose"
                :ranges="ranges"
            />
        </a-modal>

    </div>

</template>

<script>
import VSEntryVertical from './VSEntryCard/VSEntryVertical.vue';
import VSEntryHorizontal from './VSEntryCard/VSEntryHorizontal.vue';
import NormalRangesForm from './Forms/NormalRangesForm.vue';

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
        VSEntryVertical,
        VSEntryHorizontal,
        NormalRangesForm
    },

    data(){
        return {
            normalRangeVisiable: false,
            ranges:{
                temp_h: '37.5',
                temp_l: '35',
                hr_h: '130',
                hr_l: '60',
                rr_h: '60',
                rr_l: '30',
                spo2_h: '100',
                spo2_l: '90',
                bp_h: '140',
                bp_l: '86',
            }
        }
    },

    methods:{
        handleFormOpen(){
            this.normalRangeVisiable = true;
        },

        handleFormClose(rawState){
            // this.ranges = rawState;
            this.normalRangeVisiable = false;
        },
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