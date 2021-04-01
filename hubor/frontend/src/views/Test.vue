<template>
    <VSMultiViewChart/>
</template>

<style>
#card-body .ant-card-bordered{
    border-radius: 10px !important;
}
</style>

<script>
import VSMultiViewChart  from "../components/ChartsPlots/VSMultiViewChart.vue";
export default {
  name: "Home", 
  components: {
      VSMultiViewChart,
  },

  mounted(){
  }
};
</script>