<template>
    <VSAreaChart/>
</template>

<style>
#card-body .ant-card-bordered{
    border-radius: 10px !important;
}
</style>

<script>
import VSAreaChart  from "../components/ChartsPlots/VSAreaChart.vue";
export default {
  name: "Home", 
  components: {
      VSAreaChart,
  },

  mounted(){
  }
};
</script>