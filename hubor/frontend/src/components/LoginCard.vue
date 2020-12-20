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

      <a-form-item name="keeplogged">
        <a-checkbox v-model:checked="keeplogged">
          <span>Keep me logged in</span>
        </a-checkbox>
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

  mounted(){
    // if sessionid && csrftoken && keeplogged exists in cookie, redirect to dashboard
    // means the user want's to stay logged-in
    if(this.$getCookie('sessionid') != null 
      && this.$getCookie('csrftoken') != null
      && this.$getCookie('keeplogged') != null){
      this.$router.push("dashboard");
    }
  },

  data() {
    return {
      labelCol: { span: 4 },
      wrapperCol: { span: 24 },
      keeplogged: false,
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
          this.$post('api/login/', this.form)
            .then((response) =>{
              this.$store.dispatch("accounts/login", response.data)
              .then(()=>{
                // if the user wants to kept logged in. set the cookie
                if(this.keeplogged){
                  this.$setCookie('keeplogged', 1, 30);
                }

                // Route to the dash board page
                this.$router.push("dashboard");
              });
            }).catch(error =>{
                  this.$message.error("Login failed!\nPlease check you username or password.");
            })
        })
        .catch(error => {
          console.log(error);
          this.$message.error("Login failed!\nPlease check you username or password.");
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

.ant-checkbox-wrapper {
  z-index: 100;
}

#login-button{
  z-index: 100;
  opacity: 100;
  width: 200pt;
  margin-top: 50pt !important;
  border-radius: 90px !important;
	height: 40pt !important ;
}


</style>
