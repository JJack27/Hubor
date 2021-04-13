<template>
    <PendingRequestCardsGroup 
        style="width:92%; margin-top:5vh; margin-right: auto; margin-left:auto" 
    />
</template>

<style>

</style>

<script>
import PendingRequestCardsGroup from "../components/PendingRequests/PendingRequestCardsGroup.vue";
export default {
  name: "PendingRequestsPage", 
  components: {
      PendingRequestCardsGroup,
  },

  mounted(){
  }
};
</script>