<template>
  <a-form
    id='add-patient-form'
    ref="formRef"
    :model="formState"
    :rules="rules"
    v-bind="layout"
  >
    <a-form-item required has-feedback label="First name" name="first_name">
      <a-input placeholder="Frist Name" v-model:value="formState.first_name" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Last name" name="last_name">
      <a-input placeholder="Last Name" v-model:value="formState.last_name" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Email" name="email">
      <a-input placeholder="example@exa.com" v-model:value="formState.email" type="email" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Phone" name="phone">
      <a-input placeholder="7809950000" v-model:value="formState.phone" type="number" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Relationship" name="relationship">
      <a-input placeholder="child" v-model:value="formState.relationship" type="text" autocomplete="off" />
    </a-form-item>

    <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
      <a-button type="danger" @click="onDelete">Delete</a-button>
      <a-button style="margin-left: 10px" type="primary" @click="onSubmit">Submit</a-button>
      <a-button style="margin-left: 10px" type="bordered" @click="onCancel">Cancel</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { defineComponent, reactive, ref, toRaw } from 'vue';
import Axios from 'axios';
export default defineComponent({
    name:"UpdateEmergencyContactForm",
    //emits:['register-success'],
    props:[
        'patientId',
        'item',
    ],
    setup: () => {
        const formRef = ref();
        /*
        const formState = reactive({
            first_name: '',
            last_name: '',
            phone: '',
            email: '',
            relationship: '',
        });
        */

        let validatePhone = async (rule, value) => {
            if (value === '') {
                return Promise.reject('Please enter a phone number');
            }else if(value.length != 10){
                return Promise.reject('Phone number is a 10-digit number');
            }
        };

        const rules = {
            email: [
                {
                    type: 'email',
                    trigger: 'change',
                    message: "Please enter a valid email address!"
                }
            ],
            phone: [
                {
                    validator: validatePhone,
                    trigger: 'change',
                }
            ]
        };
        const layout = {
            labelCol: {
                span: 8,
            },
            wrapperCol: {
                span: 14,
            },
        };



        return {
          
          formRef,
          rules,
          layout,
        };
    },
    /// end of setup()

    data(){
        return {
            formState:{
                first_name: this.item.first_name,
                last_name: this.item.last_name,
                phone: this.item.phone,
                email: this.item.email,
                relationship: this.item.relationship,
            },
        }
    },

    methods: {
        onSubmit(){
            this.formRef
                .validate()
                .then(() => {
                    var rawState = toRaw(this.formState);
                    this.$put('/api/emergencycontactop/'+this.patientId + '/' + this.item.id + '/', rawState)
                    .then((response) => {
                        
                        rawState['patient'] = this.patientId;
                        rawState['id'] = -1;

                        var emergencyContact = JSON.parse(JSON.stringify(rawState));
                        this.$message.success("Emergency contact updated!");

                        // update the emergency contact for display
                        this.$store.dispatch('appendEmergencyContact', emergencyContact);
                        // parent components can use @add-emergency-contact-success=callback after patient was added
                        this.resetForm();
                        this.$emit("update-emergency-contact-success", "");

                    })
                    .catch((error) => {
                        console.log(error);
                        this.$message.error("Emergency contact creation failed!")
                    });
                })
                .catch(error => {
                    this.$message.error("Invalid data!")
                });
        },

        onCancel(){
            console.log("canceled");
            this.$emit("update-emergency-contact-success", "");
        },

        onDelete(){
            console.log("deleted");
            this.$emit("update-emergency-contact-success", "");
        },
    }
});
</script>

<style>
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}

#add-patient-form .ant-form-item{
    margin-bottom: 12px;
}
</style>