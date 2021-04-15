<template>
    <a-card
        class="add-emergency-contact-wrapper-card"
        :hoverable="true"
        style="border-radius: 10px !important; background:#ffffff; color:#918de0; text-align:center !important; height:100% !important;"
        @click="toEMPage"
    >
        <br/>
            <i class="fa fa-phone" aria-hidden="true" style="font-size:40pt"></i>
            <br/>
            <span style="font-size:11pt; ">Patient</span>
    </a-card>
</template>

<script>
export default{
    name: "PatientButtonCard.vue",
    components:{},
    inject:['id'],
    methods:{
        toEMPage(){
            this.$router.push('/dashboard/emergencycontact/'+ this.id);
        },

    }
}
</script>

<style>
.add-emergency-contact-wrapper-card{
    margin-top: 10pt !important;
}

</style>