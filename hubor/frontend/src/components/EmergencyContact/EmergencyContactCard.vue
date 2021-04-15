<template>
    <div>
        <a-card
            class="emergency-contact-wrapper-card"
            :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor, }"
            :hoverable="true"
            style="border-radius: 10px !important;"
            :key="item.id"
            @click="handleFormOpen"
        > 
            <h4>{{item.first_name + " " + item.last_name}}</h4>
            <p style="font-style:italic;">{{ item.relationship }}</p>

            <!-- email -->
            <a-tooltip v-if="item.email.length > 10" :title="item.email">
                <a :key="item.email" style="margin-top: -25pt !important" :href="'mailto:'+ item.email">
                    {{ `${item.email.slice(0, 10)}...` }}
                </a>
            </a-tooltip>
            <a v-else style="margin-top: -25pt !important" :href="'mailto:'+ item.email">{{ item.email }}</a>
            <br>

            <!-- phone -->
            <a style="margin-top: -25pt !important" :href="'callto:'+ item.phone">{{ item.phone }}</a>
        </a-card>

        <!-- modal for displaying detail of emergency contacts -->
        <a-modal 
            v-model:visible="showEMCVisible" 
            title="Update the Emergency Contact" 
            :footer="null"
        >
            <UpdateEmergencyContactForm 
                @update-emergency-contact-success="handleFormClose"
                :patientId = "this.id"
                :item = "this.item"  
            />
        </a-modal>
    </div>

</template>
<script>
import UpdateEmergencyContactForm from './Forms/UpdateEmergencyContactForm.vue';

export default{
    name:"EmergencyContactCard",
    components:{
        UpdateEmergencyContactForm,
    },

    inject:['id'],
    props:[
        'item'
    ],

    data(){
        return{
            showEMCVisible: false,
        }
    },

    methods:{
        handleFormClose(){
            this.showEMCVisible = false;
        },

        handleFormOpen(){
            this.showEMCVisible = true;
        },
    }
    
}
</script>