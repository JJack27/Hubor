<template>
    <div class="emergency-contact-card-wrapper">
        <h1 style="font-weight: bold; text-align: start;">
            Emergency Contact
        </h1>
        <a-row  type="flex" justify="bottom" :gutter="[16,16]">
            <a-col
                :span="8"
                v-for="item in this.dataSource"
                style="height: 180px !important;"
            >
                <EmergencyContactCard
                    :item="item"
                    style="height:100% !important;"
                />
            </a-col>
            
            <!-- card button for adding new emergency contact -->
            <a-col
                :span="8"
                v-if="this.dataSource.length <= 2"
                @click="showAddEmergencyContactModal"
                style="height: 180px !important;"
            >
                <a-card
                    class="add-emergency-contact-wrapper-card"
                    :hoverable="true"
                    style="border-radius: 10px !important; background:#918de0; color:#ffffff; text-align:center !important; height:100% !important;"

                > 
                    <span style="font-size:60pt; ">+</span>
                    
                </a-card>
            </a-col>
        </a-row>
        
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
import AddEmergencyContactForm from './Forms/AddEmergencyContactForm.vue';
import EmergencyContactCard from './EmergencyContactCard.vue';
import {UserOutlined} from '@ant-design/icons-vue';

export default{
    name: "EmergencyContactCardsGroup",
    components:{
        UserOutlined,
        AddEmergencyContactForm,
        EmergencyContactCard
    },
    inject:['id'],
    props:[
        'dataSource'
    ],

    setup(){
        const pagination = {
            pageSize: 3,
        };

        return {
            pagination,
        }
    },

    mounted(){
    },

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

.emergency-contact-wrapper-card{
    margin-top: 10pt !important;
    text-align: start !important;
}

.emergency-contact-wrapper-card .ant-card{
    border-radius: 10px !important;
}


.ant-card.ant-card-bordered.emergency-contact-wrapper-card{
    height: 100%
}

/*
.ant-card.ant-card-bordered.ant-card-hoverable.emergency-contact-wrapper-card{
    height: 100%;
}
*/



</style>