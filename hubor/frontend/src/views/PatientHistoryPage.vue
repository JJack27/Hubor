<template>
    <div>
        <VSLineRangedChart />
    </div>
</template>

<script>
import VSLineRangedChart from '../components/ChartsPlots/VSLineRangedChart.vue';

export default{
    name:"PatientHistoryPage",
    inject:['id', ],

    components:{
        VSLineRangedChart,
    },

    setup(){

    },

    mounted(){
        console.log(this.id);
    }
}
</script>

<style>

</style>