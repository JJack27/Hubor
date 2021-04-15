<template>
    <div>
        <h1 style="font-weight: bold; text-align: start;">
            {{ this.item.first_name + ' '+ this.item.last_name}}
        </h1>

        <!-- contact information cards -->
        <!-- phone call -->
        <ContactInformationCard
            icon="fa fa-phone"
            :href="'callto:' + item.phone"
            :content="item.phone"
        />
        <br/>
        <!-- email -->
        <ContactInformationCard
            icon="fa fa-envelope"
            :href="'mailto:' + item.email"
            :content="item.email"
        />

    </div>
</template>

<script>
import ContactInformationCard from "./Cards/ContactInformationCard.vue";

export default{
    name:"PatientContactCardsGroup",
    inject:['id'],
    components:{
        ContactInformationCard,
    },

    data(){
        return {
            item: this.$store.getters.patients[this.id],
        }
    },

    
}
</script>

<style>
</style>