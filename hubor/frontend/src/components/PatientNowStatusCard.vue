<template>
    <div class="patient-now-status-card">
        
        <a-row type="flex" justify="space-between"
            style="font-weight: bold; font-size:14pt;"
        >
            <a-col :span="8" style="text-align: start">Current Vitals</a-col>
            <a-col :span="14" style="text-align: end">{{ this.currentTime }}</a-col>
        </a-row>
        <!-- this.$store.getters.patients[this.id].hr -->
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="12">
                <VSEntryVertical
                    icon="hr_icon.png"
                    :value="this.auto['hr']"
                    vs="hr"
                    unit="bpm"
                    title="Heart Rate"
                    @switch-to-history="handleSwitch"
                />
            </a-col>

            <a-col :span="12">
                <VSEntryVertical
                    icon="temp_icon.png"
                    :value="this.auto['temp']"
                    vs="temp"
                    unit="°C"
                    title="Temperature"
                    @switch-to-history="handleSwitch"
                />
            </a-col>
        </a-row>

        <!-- SPO2 -->
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="12">
                <VSEntryVertical
                    icon="spo2_icon.png"
                    :value="this.auto['spo2']"
                    vs="spo2"
                    unit="%"
                    title="O<sub>2</sub> Saturation"
                    @switch-to-history="handleSwitch"
                />
            </a-col>

            <!-- RR -->
            <a-col :span="12">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="this.auto['rr']"
                    vs="rr"
                    unit="rpm"
                    title="Respiration Rate"
                    @switch-to-history="handleSwitch"
                />
            </a-col>
        </a-row>

        
        

        <!-- BP -->
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="24">
                <VSEntryHorizontal
                    icon="bp_icon.png"
                    :value="this.auto['bp_l'] + '/' + this.auto['bp_h']"
                    unit="mmHg"
                    vs="bp"
                    title="Blood Pressure"
                    @switch-to-history="handleSwitch"
                />
            </a-col>
        </a-row>

        

        
        
        
    </div>
</template>

<script>
import VSEntryVertical from './VSEntryCard/VSEntryVertical.vue';
import VSEntryHorizontal from './VSEntryCard/VSEntryHorizontal.vue';
export default{
    name: "PatientNowStatusCard",
    components:{
        VSEntryVertical,
        VSEntryHorizontal,
    },
    data(){
        return {
            auto:{
                hr: 72,
                rr: 16,
                temp: 36.4,
                spo2: 95,
                bp_h: 67,
                bp_l: 110
            },
            timeTask: null,
            currentTime: new Date().toLocaleString('en-us'),
            autoTask: null,
        }
    },

    inject:['id'],
    methods:{
        updateTime(){
            this.currentTime = new Date().toLocaleString('en-us');
        },
        // method to handle event when user click on now-status-card
        // switch to history
        handleSwitch(vs){
            this.$emit('switch-to-history',vs);
        },
        updateVS(){
            var range = {
                hr:{l:70, h:5},
                rr:{l:16, h:5},
                temp:{l:36.4, h:0.6},
                spo2:{l:95, h:5},
                bp_l:{l:67, h:5},
                bp_h:{l:110, h:5},
            };

            for(var i in this.auto){
                if(i == 'temp'){
                    if(Math.random()>0.5){
                        this.auto[i] = ((Math.random() * range[i]['h']) + range[i]['l']).toFixed(1);
                    }else{
                        this.auto[i] = (range[i]['l'] - (Math.random() * range[i]['h']) ).toFixed(1);
                    }
                    
                }else{
                    if(Math.random() > 0.5){
                        this.auto[i] = Math.floor(Math.random() * range[i]['h']) + range[i]['l'];
                    }else{
                        this.auto[i] = range[i]['l'] - Math.floor(Math.random() * range[i]['h']);
                    }
                    
                }
            }
        }
    },
    mounted(){
        this.autoTask = setInterval(this.updateVS, 3000);
        this.timeTask = setInterval(this.updateTime, 1000);
    },

    beforeUnmounted(){
        clearInterval(this.autoTask);
        this.autoTask = null;
    },

    
    //this.$store.getters.patients[this.id].bp_h + '/' + this.$store.getters.patients[this.id].bp_l
}
</script>

<style>
.patient-now-status-card .ant-card-bordered{
    border-radius: 10px !important;
}
</style>