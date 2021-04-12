<template>
<div class="patient-info-card">
    <a-card >
        <a-descriptions title="User Info" bordered>
            <a-descriptions-item label="Name" :span="3">
                {{this.$store.getters.patients[this.id].first_name + " " + this.$store.getters.patients[this.id].last_name}}
            </a-descriptions-item>
            <a-descriptions-item label="ID" :span="3">{{this.id}}</a-descriptions-item>
            <a-descriptions-item label="Email" :span="3">{{this.$store.getters.patients[this.id].email}}</a-descriptions-item>

            <a-descriptions-item label="Height" :span="1">{{this.$store.getters.patients[this.id].height}} CM</a-descriptions-item>
            <a-descriptions-item label="Weight" :span="2">{{this.$store.getters.patients[this.id].weight}} KG</a-descriptions-item>
            
            <a-descriptions-item label="Date of Birth">{{this.$store.getters.patients[this.id].date_of_birth}}</a-descriptions-item>
            <a-descriptions-item label="Phone" :span="2">{{this.$store.getters.patients[this.id].phone}}</a-descriptions-item>
            
            <a-descriptions-item label="Facility" :span="3">
                <div v-if="this.$store.getters.patients[this.id].facility != 'null'">
                    <span style="font-weight:bold">{{this.$store.getters.patients[this.id].facility.name}}</span>
                    <br/>
                    <br/>
                    <HomeFilled /> {{this.$store.getters.patients[this.id].facility.address}}
                    <br/>
                    <PhoneFilled /> {{this.$store.getters.patients[this.id].facility.phone}}
                </div>
                <div v-else>
                    This patient doesn't belong to any health care facilities.
                </div>
                
            </a-descriptions-item>

            <a-descriptions-item label="Notes" :span="3">
                {{ this.$store.getters.patients[this.id].notes}}
            </a-descriptions-item>
        </a-descriptions>
        
        <br/>
        <h3>Emergency Contacts</h3>
        
        <a-table
            :columns="emergency_contacts_columns"
            :dataSource="this.$store.getters.patients.[this.id].emergency_contacts"
            :pagination="false"
        />
        
        <div v-if="this.$store.getters.patients.[this.id].emergency_contacts.length == 0">
            This patient has no emergency contacts.
        </div>
        <br/>
        <a-button type="primary" 
            v-if="this.$store.getters.patients.[this.id].emergency_contacts.length >= 0 && this.$store.getters.patients.[this.id].emergency_contacts.length <= 2"
            @click="showAddEmergencyContactModal"
        >
            + Add an emergency contact
        </a-button>

        <a-modal 
            v-model:visible="addEmergencyContactVisible" 
            title="Add an Emergency Contact" 
            :footer="null">
            <AddEmergencyContactForm 
                @add-emergency-contact-success="handleFormClose"
                :patientId = "this.id"    
            />
        </a-modal>
    </a-card>
</div>

</template>

<script>

import {PhoneFilled, HomeFilled} from '@ant-design/icons-vue';
import AddEmergencyContactForm from './Forms/AddEmergencyContactForm.vue';

export default{
    name: "PatienInfoCard",
    inject:['id'],

    components:{
        PhoneFilled,
        HomeFilled,
        AddEmergencyContactForm,
    },

    data(){
        return {
            addEmergencyContactVisible: false,
        }
    },

    methods:{
        showAddEmergencyContactModal(){
            this.addEmergencyContactVisible = true;
        },

        handleFormClose(patientId){
            this.addEmergencyContactVisible = false;
        },

    },

    setup() {
      return {
        emergency_contacts_columns: [
                {
                    title: 'First Name',
                    dataIndex: 'first_name',
                    key: 'first_name',
                },
                {
                    title: 'Last Name',
                    dataIndex: 'last_name',
                    key: 'last_name',
                },
                {
                    title: 'Phone',
                    dataIndex: 'phone',
                    key: 'phone',
                },
                {
                    title: 'Email',
                    dataIndex: 'email',
                    key: 'email',
                },
            ]
      };
    },


}
</script>

<style>
.patient-info-card .ant-card-bordered{
    border-radius: 10px !important;
    text-align: start !important;
}
</style>