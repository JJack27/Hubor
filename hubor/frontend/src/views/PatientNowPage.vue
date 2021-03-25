<template>
    <div>
        Now Page
        {{ this.$route.params.id }}
    </div>
</template>

<script>
import PatientInfoCard from "../components/PatientInfoCard.vue";
import PatientNowStatusCard from "../components/PatientNowStatusCard.vue";

export default{
    name:"PatientNowPage",
    components:{
        PatientNowStatusCard,
        PatientInfoCard,
    },

    props:[
        'id',
    ]
}
</script>

<style>

</style>