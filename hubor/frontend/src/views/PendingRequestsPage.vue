<template>
    <PendingRequestListCard 
        style="width:92%; margin-top:5vh; margin-right: auto; margin-left:auto" 
    />
</template>

<style>

</style>

<script>
import PendingRequestListCard from "../components/PendingRequestListCard.vue";
export default {
  name: "PendingRequestsPage", 
  components: {
      PendingRequestListCard,
  },

  mounted(){
  }
};
</script>