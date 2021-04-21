<template>
    <div class="patient-now-status-card">
        <h1 style="font-weight: bold; text-align: start;">
            Current Status
        </h1>
        <!-- this.$store.getters.patients[this.id].hr -->
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="12">
                <VSEntryVertical
                    icon="hr_icon.png"
                    :value="this.auto['hr']"
                    unit="bpm"
                    title="Heart Rate"
                />
            </a-col>

            <a-col :span="12">
                <VSEntryVertical
                    icon="temp_icon.png"
                    :value="this.auto['temp']"
                    unit="°C"
                    title="Temperature"
                />
            </a-col>
        </a-row>

        <!-- SPO2 -->
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="12">
                <VSEntryVertical
                    icon="spo2_icon.png"
                    :value="this.auto['spo2']"
                    unit="%"
                    title="Oxygen Saturation"
                />
            </a-col>

            <!-- RR -->
            <a-col :span="12">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="this.auto['rr']"
                    unit="rpm"
                    title="Respiration Rate"
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
                    title="Blood Pressure"
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
            autoTask: null,
        }
    },

    inject:['id'],
    methods:{
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
    },

    beforeUnmounted(){
        clearInterval(this.autoTask);
        this.autoTask = null;
    }
    //this.$store.getters.patients[this.id].bp_h + '/' + this.$store.getters.patients[this.id].bp_l
}
</script>

<style>
.patient-now-status-card .ant-card-bordered{
    border-radius: 10px !important;
}
</style>