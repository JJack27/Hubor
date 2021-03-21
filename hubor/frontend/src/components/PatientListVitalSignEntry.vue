<template>
    <a-row>
        <a-col :span="6">
            <img
                :src="require(`@/assets/icons/${this.icon}`)"
                height="40"
                width="40"
                class="list-item-icon">
        </a-col>
         <a-col :span="4">
            <span class="vital-sign-data">{{this.value}}</span>
            <br>
            <span class="vital-sign-unit">{{this.unit}}</span>
        </a-col>
    </a-row>
</template>

<script>
export default {
    name: "PatientListVitalSignEntry",
    props: ['icon', 'value', 'unit']
}
</script>

<style>
.vital-sign-data{
    font-size: 20pt;
    margin:0;
    padding:0;
}

.vital-sign-unit{
    font-size:8pt;
    padding-top:-15px;
}
</style>