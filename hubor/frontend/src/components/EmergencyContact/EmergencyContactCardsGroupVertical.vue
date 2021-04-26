<template>
    <div>
        <h1 style="font-weight: bold; text-align: start;">
            Emergency Contacts
        </h1>
        <!-- a list of emergency contacts cards -->
        <div
            v-if="this.$store.getters.patients[this.$route.params.id].emergency_contacts.length > 0"
            v-for="item in this.$store.getters.patients[this.$route.params.id].emergency_contacts"
            :key="item.id"
        >
            <EMContactInformationCard 
                :item="item"
            />
        </div>

        <!-- show empty if there is no data -->
        <div v-else>
            <a-empty />
        </div>

        <!-- card button for adding new emergency contacts -->
        <AddEMButtonCard/>
        
    </div>
</template>

<script>
import EMContactInformationCard from './Cards/EMContactInformationCard.vue';
import AddEMButtonCard from './ButtonCard/AddEMButtonCard.vue';
export default{
    name:"EmergencyContactCardsGroupVertical",
    components:{
        EMContactInformationCard,
        AddEMButtonCard,
    },

    data(){
        return {
            contacts: this.$store.getters.patients[this.$route.params.id].emergency_contacts,
            id: this.$route.params.id,
        }
    },

    methods:{
        backToDashboard(){
            window.alert("wrong!")
        }
    },

    mounted(){
        console.log(this.contacts);
    },


    
}
</script>

<style>
</style>