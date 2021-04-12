<template>
    <div class="patient-now-status-card">
        <h1 style="font-weight: bold">
            Current Status
        </h1>
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="12">
                <VSEntryVertical
                    icon="hr_icon.png"
                    :value="this.$store.getters.patients[this.id].hr"
                    unit="bpm"
                    title="Heart Rate"
                />
            </a-col>

            <a-col :span="12">
                <VSEntryVertical
                    icon="temp_icon.png"
                    :value="this.$store.getters.patients[this.id].temp"
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
                    :value="this.$store.getters.patients[this.id].spo2"
                    unit="%"
                    title="Oxygen Saturation"
                />
            </a-col>

            <!-- RR -->
            <a-col :span="12">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="this.$store.getters.patients[this.id].rr"
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
                    :value="this.$store.getters.patients[this.id].bp_h + '/' + this.$store.getters.patients[this.id].bp_l"
                    unit="mmHg"
                    title="Blood Pressure"
                />
            </a-col>
        </a-row>

        

        
        
        
    </div>
</template>

<script>
import VSEntryVertical from './PatientStatusEntryCard/VSEntryVertical.vue';
import VSEntryHorizontal from './PatientStatusEntryCard/VSEntryHorizontal.vue';
export default{
    name: "PatientNowStatusCard",
    components:{
        VSEntryVertical,
        VSEntryHorizontal,
    },

    inject:['id'],
    
    mounted(){
    }
    //this.$store.getters.patients[this.id].bp_h + '/' + this.$store.getters.patients[this.id].bp_l
}
</script>

<style>
.patient-now-status-card .ant-card-bordered{
    border-radius: 10px !important;
}
</style>