<template>
    <a-card
        class="vs-entry-wrapper-card"
        :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor}"
        :hoverable="false"
    >
        <a-row align="middle">
            <a-col :span="8">
                <img
                    :src="require(`@/assets/icons/diagnosis-icon.jpg`)"
                    height="60"
                    width="60"
                    class="list-item-icon">
            </a-col>
            <a-col :span="16">
                <span class="vs-title">Diagnosis</span>
                <br>
                <diagnosis-tag-group/>
            </a-col>
        </a-row>
    </a-card>
</template>

<script>
import DiagnosisTagGroup from './DiagnosisTagGroup.vue'

export default {
    name: "DiagnosisCardHorizontal",
    components:{
        DiagnosisTagGroup,
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