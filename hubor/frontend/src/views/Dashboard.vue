<template>
  <a-layout id="components-layout-demo-responsive">
    <a-layout-sider
      breakpoint="lg"
      collapsed-width="0"
      @collapse="onCollapse"
      @breakpoint="onBreakpoint"
    >
      <div class="logo">
        <p id="logo-text">
            MITACS<br>Vital Sign Project
        </p>
      </div>
      <a-menu theme="dark" mode="inline" v-model:selectedKeys="selectedKeys">
        <a-menu-item key="1">
          <user-outlined />
          <span class="nav-text">nav 1</span>
        </a-menu-item>
        <a-menu-item key="2">
          <video-camera-outlined />
          <span class="nav-text">nav 2</span>
        </a-menu-item>
        <a-menu-item key="3">
          <upload-outlined />
          <span class="nav-text">nav 3</span>
        </a-menu-item>
        <a-menu-item key="4">
          <user-outlined />
          <span class="nav-text">nav 4</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header :style="{ background: '#fff', padding: 0 }">
        
      </a-layout-header>
      <a-layout-content :style="{ margin: '24px 16px 0' }">
        <div :style="{ padding: '24px', background: '#fff', minHeight: '83vh'}">
          content
        </div>
      </a-layout-content>
      <a-layout-footer style="textAlign: center; bottom:0;">
        Vital Sign Project ©2021 Created by Yizhou Zhao
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>


<script>
import { UserOutlined, VideoCameraOutlined, UploadOutlined } from '@ant-design/icons-vue';

export default {
    name: "Dashboard",

    data() {
        return {
            selectedKeys: ['4'],
        };
    },
    components: {
        UserOutlined,
        VideoCameraOutlined,
        UploadOutlined,
    },

    mounted(){
        /*
        // redirect user to the login page if the sessionid and csrtoken doesn't exist
        if(this.$getCookie('sessionid') === null
            && this.$getCookie('csrftoken') === null){
            this.$router.push('/');
        }else{
            // if currentUserInfo is empty but the session exists. Get from the server
            this.$get('api/myinfo/')
                .then((response) => {
                    // update user info in the store.
                    this.$store.dispatch('accounts/login', response.data);
                }).catch((error) =>{
                    // redirect it to the home page if getting error
                    console.log(error);
                    this.$router.push('/');
                })
        }
        */
    },

    methods: {
    onCollapse(collapsed, type) {
      console.log(collapsed, type);
    },
    onBreakpoint(broken) {
      console.log(broken);
    },
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');
#components-layout-demo-responsive .logo {
  height: 32px;
  margin: 16px;
  margin-bottom: 40pt;
}

#logo-text{
    color: #e6f6ff;
    font-family: 'Do Hyeon', sans-serif;
    font-size: 15pt;
}
</style>