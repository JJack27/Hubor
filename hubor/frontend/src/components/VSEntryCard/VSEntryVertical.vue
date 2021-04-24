<template>
    <a-card
        class="vs-entry-wrapper-card"
        :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor}"
        :hoverable="true"
        @click="switchToHistory"
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
            <a-col class="vs-unit" :span="8">
                <span >{{this.unit}}</span>
            </a-col>
        </a-row>

    </a-card>
</template>

<script>
export default {
    name: "VSEntryVertical",
    props: ['icon', 'value', 'unit', 'background', 'color', 'title', 'vs'],
    emits:['switch-to-history'],
    methods:{
        switchToHistory(){
            this.$emit("switch-to-history", this.vs);
        },
    }
}
</script>

<style>
.vs-data{
    font-size: 26pt;
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
</style>