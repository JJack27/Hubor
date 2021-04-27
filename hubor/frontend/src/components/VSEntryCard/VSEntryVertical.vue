<template>
    <a-card
        class="vs-entry-wrapper-card"
        :hoverable="true"
        @click="switchToHistory"
        :class="this.abnormal"
    >
        <a-row type="flex" justify="center" align="bottom">
            <a-col :span="4">
                <img
                    :src="require(`@/assets/icons/${this.icon}`)"
                    height="30"
                    width="30"
                    class="list-item-icon">
            </a-col>
            <a-col :span="20" class="vs-title" v-html="this.title">
                
            </a-col>
            
        </a-row>
        <a-row type="flex" justify="center" align="bottom">
            <a-col class="vs-data" :span="16">
                <span >{{this.value}}</span>
            </a-col>
            <a-col class="vs-data" :span="4" style="text-align:end">
                <span >{{this.arterial}}</span>
            </a-col>
            <a-col class="vs-unit" :span="4">
                <span >{{this.unit}}</span>
            </a-col>
        </a-row>

    </a-card>
</template>

<script>
export default {
    name: "VSEntryVertical",
    props: ['icon', 'value', 'unit', 'background', 'color', 'title', 'vs','arterial'],
    emits:['switch-to-history'],
    methods:{
        switchToHistory(){

            this.$emit("switch-to-history", this.vs);
        },
    },
    computed: {
        abnormal(){
            // TEMP: if vs is bp, return white
            if(this.vs == 'bp'){
                return "normal-vs";
            }
            // check if abnormal
            var lowerBound = this.$store.getters.patients[this.$route.params.id].normal_range[this.vs+'_l'];
            var upperBound = this.$store.getters.patients[this.$route.params.id].normal_range[this.vs+'_h'];
            if(this.value <= lowerBound || this.value >= upperBound){
                return "abnormal-vs"
            }else{
                return "normal-vs"
            }
        }
    },
}
</script>

<style>
.vs-data{
    font-size: 22pt;
    font-weight:bold;
    color: #0a0956;
    margin-top:10px;
    padding-top: 10px;
}

.vs-unit{
    font-size: 8pt;
    text-align: end !important;
    font-weight: bold;
    padding-bottom: 13px !important;
}

.vs-title{
    font-size: 12pt;
    text-align: end;
    color: #aaaaaa;
    font-weight:bold;
}

.vs-entry-wrapper-card{
    text-align: start;
}

.vs-entry-wrapper-card .ant-card-body{
    padding-top: 12px;
    padding-bottom: 12px;
}

.abnormal-vs {
    background: #ffd4d6;
}

.normal-vs{
    background: #fff;
}
</style>