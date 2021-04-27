<template>
    <div class="patient-history-card">
        
        <a-row type="flex" justify="space-between"
            style="font-weight: bold; font-size:14pt;"
        >
            <a-col :span="14" style="text-align: start">{{ new Date(this.time).toLocaleString() }}</a-col>
        </a-row>
        <!-- this.$store.getters.patients[this.$route.params.id].hr -->
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="8">
                <VSEntryVertical
                    icon="hr_icon.png"
                    :value="this.hr.toFixed(1)"
                    vs="hr"
                    unit="bpm"
                    title="Heart Rate"
                    @switch-to-history="handleSwitch"
                />
            </a-col>
            
            <!-- temp -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="temp_icon.png"
                    :value="this.temp.toFixed(1)"
                    vs="temp"
                    unit="°C"
                    title="Temperature"
                    @switch-to-history="handleSwitch"
                />
            </a-col>

            <!-- SPO2 -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="spo2_icon.png"
                    :value="this.spo.toFixed(1)"
                    vs="spo2"
                    unit="%"
                    title="O<sub>2</sub> Saturation"
                    @switch-to-history="handleSwitch"
                />
            </a-col>
        </a-row>

        
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <!-- RR -->
            <a-col :span="8">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="this.rr.toFixed(1)"
                    vs="rr"
                    unit="rpm"
                    title="Respiration<br/>Rate"
                    @switch-to-history="handleSwitch"
                />
            </a-col>

            <!-- BP -->
            <a-col :span="16">
                <VSEntryVertical
                    icon="bp_icon.png"
                    :value="this.bpl.toFixed(1) + '/' + this.bph.toFixed(1)"
                    unit="mmHg"
                    vs="bp"
                    title="Blood<br/>Pressure"
                />
            </a-col>
        </a-row>        
    </div>
</template>


<script>
import VSEntryVertical from '../VSEntryCard/VSEntryVertical.vue';
import VSEntryHorizontal from '../VSEntryCard/VSEntryHorizontal.vue';
export default{
    name: "VSHistoryCardGroup",
    components:{
        VSEntryVertical,
        VSEntryHorizontal,
    },
    props:[
        'rr',
        'hr',
        'bpl',
        'bph',
        'spo',
        'temp',
        'time'
    ],
    data(){
        return {
        }
    },

    inject:['id'],
    methods:{
        handleSwitch(vs){
            this.$emit('switch-to-history', vs);
        }
    },
    mounted(){
    },

    beforeUnmounted(){
    },

    
    //this.$store.getters.patients[this.$route.params.id].bp_h + '/' + this.$store.getters.patients[this.$route.params.id].bp_l
}
</script>

<style>
.patient-history-card .ant-card-bordered{
    border-radius: 10px !important;
}
</style>