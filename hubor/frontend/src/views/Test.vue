<template>
    <VSLineRangedChart/>
</template>

<style>
#card-body .ant-card-bordered{
    border-radius: 10px !important;
}
</style>

<script>
import VSLineRangedChart  from "../components/ChartsPlots/VSLineRangedChart.vue";
export default {
  name: "Home", 
  components: {
      VSLineRangedChart,
  },

  mounted(){
  }
};
</script>