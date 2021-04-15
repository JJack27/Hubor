<template>
    <div>
        <a-card
            class="add-emergency-contact-wrapper-card"
            :hoverable="true"
            style="border-radius: 10px !important; background:#fff; color:#918de0; text-align:center !important; height:100% !important;"
            @click="showAddEmergencyContactModal"
        >   
            <br/>
            <i class="fa fa-user-plus" aria-hidden="true" style="font-size:40pt; "></i>
            <br/>
            <span style="font-size:11pt">Add a contact</span>           
        </a-card>

        <!-- modal for adding emergency contact -->
        <a-modal 
            v-model:visible="addEmergencyContactVisible" 
            title="Add an Emergency Contact" 
            :footer="null">
            <AddEmergencyContactForm 
                @add-emergency-contact-success="handleFormClose"
                :patientId = "this.id"    
            />
        </a-modal>
    </div>
</template>
<script>
import AddEmergencyContactForm from '../Forms/AddEmergencyContactForm.vue';

export default{
    name: "AddEMButtonCard",
    components:{
        AddEmergencyContactForm,
    },

    inject: ['id'],
    data(){
        return{
            addEmergencyContactVisible: false,
        };
    },

    methods:{
        showAddEmergencyContactModal(){
            this.addEmergencyContactVisible = true;
        },

        handleFormClose(patientId){
            this.addEmergencyContactVisible = false;
        },

    }

}

</script>

<style>
.add-emergency-contact-wrapper-card{
    margin-top: 10pt !important;
}

</style>