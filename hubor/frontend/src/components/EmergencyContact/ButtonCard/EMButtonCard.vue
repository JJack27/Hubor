<template>
    <div>
        <a-card
            class="add-emergency-contact-wrapper-card"
            :hoverable="true"
            style="border-radius: 10px !important; background:#fff; color:#918de0; text-align:center !important; height:100% !important;"
            @click="toEMPage"
        >   
            <br/>
            <i class="fa fa-phone" aria-hidden="true" style="font-size:40pt"></i>
            <br/>
            <span style="font-size:11pt; ">Caregivers</span>
        </a-card>
    </div>
</template>

<script>
export default{
    name: "EMButtonCard.vue",
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