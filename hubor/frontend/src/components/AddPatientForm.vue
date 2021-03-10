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

    <a-form-item required has-feedback label="Username" name="username">
      <a-input placeholder="Username" v-model:value="formState.username" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Height" name="height">
      <a-input placeholder="in CM" v-model:value="formState.height" type="number" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Weight" name="weight">
      <a-input placeholder="in KG" v-model:value="formState.weight" type="number" autocomplete="off" />
    </a-form-item>

    
    

    <a-form-item required has-feedback label="Email" name="email">
      <a-input placeholder="example@exa.com" v-model:value="formState.email" type="email" autocomplete="off" />
    </a-form-item>

    <a-form-item required has-feedback label="Phone" name="phone">
      <a-input placeholder="7809950000" v-model:value="formState.phone" type="number" autocomplete="off" />
    </a-form-item>


    <a-form-item required has-feedback label="Date of Birth" name="date_of_birth" >
      <a-date-picker
        v-model:value="formState.date_of_birth"
        type="date"
        placeholder="Pick a date"
        style="width: 100%"
      />
    </a-form-item>

    <a-form-item required label="Gender" name="gender">
      <a-select v-model:value="formState.gender" placeholder="Pick your gender">
        <a-select-option value=0>Male</a-select-option>
        <a-select-option value=1>Female</a-select-option>
      </a-select>
    </a-form-item>


    <a-form-item required has-feedback label="Password" name="password">
      <a-input v-model:value="formState.password" type="password" autocomplete="off" />
    </a-form-item>
    <a-form-item has-feedback label="Confirm" name="checkPass">
      <a-input v-model:value="formState.checkPass" type="password" autocomplete="off" />
    </a-form-item>
    <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
      <a-button type="primary" @click="onSubmit">Submit</a-button>
      <a-button style="margin-left: 10px" @click="resetForm">Reset</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { defineComponent, reactive, ref, toRaw } from 'vue';
import Axios from 'axios';
export default defineComponent({
    //emits:['register-success'],
    //props:['patientId'],
    setup: () => {
        const formRef = ref();
        const formState = reactive({
            first_name: '',
            password: '',
            checkPass: '',
            date_of_birth: undefined,
            user_type: 0,
            gender: "",
            height: '',
            weight: '',
            phone: undefined,
            notes: '',
        });
    

        let validatePass = async (rule, value) => {
            if (value === '') {
                return Promise.reject('Please input the password');
            } else {
                if (formState.checkPass !== '') {
                formRef.value.validateField('checkPass');
                }

                return Promise.resolve();
            }
        };

        let validatePass2 = async (rule, value) => {
            if (value === '') {
                return Promise.reject('Please input the password again');
            } else if (value !== formState.password) {
                return Promise.reject("Two inputs don't match!");
            } else {
                return Promise.resolve();
            }
        };

        let validateEmail = async (rule, value) => {
            if (value === '') {
                return Promise.reject('Please enter an valid email address');
            }else{
                return Axios.get('api/emailvalidation/'+value+ '/')
                    .then((response)=>{
                        return Promise.resolve();
                    }).catch((error)=>{
                        return Promise.reject("Email address is already in use!");
                    })
            }

        };

        let validatePhone = async (rule, value) => {
            if (value === '') {
                return Promise.reject('Please enter a phone number');
            }else if(value.length != 10){
                return Promise.reject('Phone number is a 10-digit number');
            }else{
                return Axios.get('api/phonevalidation/'+value+ '/')
                    .then((response)=>{
                        return Promise.resolve();
                    }).catch((error)=>{
                        return Promise.reject("This phone number is already in use!");
                    });
            }
        };

        let validateUsername = async (rule, value) => {
            if (value === '') {
                return Promise.reject('Please enter a valid username');
            }else{
                var usernameRegex = /[a-zA-Z0-9][a-zA-Z0-9_]{3,}/;
                if(!value.match(usernameRegex)){
                    return Promise.reject("Username has to be at least 4 characters long.\nAccepting digits, characters, and unserscore")
                }
                
                return Axios.get('api/usernamevalidation/'+value+'/')
                    .then((response)=>{
                        return Promise.resolve();
                    }).catch((error)=>{
                        return Promise.reject("This username is already in use!");
                    });
            }
        }


        const rules = {
            password: [
                {
                validator: validatePass,
                trigger: 'change',
                },
            ],
            checkPass: [
                {
                    validator: validatePass2,
                    trigger: 'change',
                },
            ],
            date_of_birth: [
                {
                    required: true,
                    message: 'Please pick a date',
                    trigger: 'change',
                    type: 'object',
                },
            ],
            email: [
                {
                    validator: validateEmail,
                    trigger: 'change',
                    
                },
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
            ],
            username: [
                {
                    validator: validateUsername,
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

        const resetForm = () => {
        formRef.value.resetFields();
        };


        return {
        formState,
        formRef,
        rules,
        layout,
        resetForm,
        };
    },
    /// end of setup()

    methods: {
        onSubmit(){
            this.formRef
                .validate()
                .then(() => {
                    var rawState = toRaw(this.formState);
                    rawState.date_of_birth = rawState.date_of_birth.toString();
                    var pid = this.patientid;
                    this.$post('api/register/', rawState)
                    .then((response) => {
                        this.resetForm();
                        pid = response.data.data.id;
                        // parent components can use @register-success=callback after patient was added
                        this.$emit("register-success", pid);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
                })
                .catch(error => {
                console.log('error', error);
                });
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