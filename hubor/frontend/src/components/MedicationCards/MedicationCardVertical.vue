<template>
    <a-card
        class="vs-entry-wrapper-card"
        :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor}"
        :hoverable="false"
    >
        <a-row type="flex" justify="start" align="bottom">
            <a-col :span="2">
                <img
                    :src="require(`@/assets/icons/rx-icon.png`)"
                    height="30"
                    width="30"
                    class="list-item-icon">
            </a-col>
            <a-col :span="22" class="med-title">
                Medications
            </a-col>
            
        </a-row>
        <a-row type="flex" justify="start" align="bottom">
            <medication-tag-group id="medication-tags"/>
        </a-row>

    </a-card>
</template>

<script>
import MedicationTagGroup from './MedicationTagGroup.vue'
export default {
    name: "MedicationCardVertical",
    injects:['id'],
    components:{
        MedicationTagGroup,
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

.med-title{
    font-size: 12pt;
    text-align: start;
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

#medication-tags{
    margin-top: 15pt;
}
</style>