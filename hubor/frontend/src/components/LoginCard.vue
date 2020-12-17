<template>
  
    <a-form 
      ref='loginFormRef'
      :model="form" 
      :rules="rules"
      :wrapper-col="wrapperCol">
      <!-- Login Identification = email / username -->
      <a-form-item required name="username">
        <a-input v-model:value="this.form.username" placeholder="Username">
          <template #prefix><UserOutlined :style="{fontSize: '16px', color: '#918de0'}"/></template>
        </a-input>
      </a-form-item>

      <!-- Password -->
      <a-form-item required name="password">
        <a-input-password type v-model:value="this.form.password" placeholder="Password">
          <template #prefix><LockOutlined :style="{fontSize: '16px', color: '#918de0'}"/></template>
        </a-input-password>
      </a-form-item>

      <a-form-item >
        <a-button id="login-button" type="primary" @click="onSubmit">
          Login
        </a-button>
      </a-form-item>
    </a-form>
  
</template>


<script>
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue';
export default {
  name:"LoginCard",

  components:{
    UserOutlined,
    LockOutlined
  },

  data() {
    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 24 },
      form: {
        username: '',
        password: '',
      },

      rules:{
        username: [
          {required: true, message: "Please enter your username!", trigger:'blur'},
        ],

        password: [
          {required: true, message: "Please enter your password!", trigger: 'blur'}
        ]
      }
       
    };
  },
  methods: {
    onSubmit() {
      this.$refs.loginFormRef
        .validate()
        .then(() => {
          console.log('values', this.form);
        })
        .catch(error => {
          console.log('error', error);
        });
    },
  },
};
</script>

<style>
.ant-card-body{
  padding-bottom:0px
}

.ant-input {
	border-radius: 90px !important;
	height: 40pt !important ;
  z-index: 100;
}

.ant-input-affix-wrapper{
  border-radius: 90px !important;
  z-index: 100; 
}

#login-button{
  z-index: 100;
  opacity: 100;
  width: 200pt;
  margin-top: 25% !important;
  border-radius: 90px !important;
	height: 40pt !important ;
}


</style>
