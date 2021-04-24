<template>
  <a-layout id="components-layout-demo-responsive">
    <a-layout-sider
      breakpoint="lg"
      collapsed-width="0"
      @collapse="onCollapse"
      @breakpoint="onBreakpoint"
    >
      <div class="logo" style="text-align: start;">
        <p id="logo-text">
            Life <br>
            Zenzers
        </p>
      </div>
      <a-menu theme="dark" mode="inline" v-model:selectedKeys="selectedKeys" style="text-align:start">
        <a-menu-item key="1">
          <ProfileFilled />
          <span class="nav-text">Patients</span>
        </a-menu-item>

        <a-menu-item key="2">
          <ExclamationCircleFilled />
          <span class="nav-text">Notifications</span>
        </a-menu-item>

        <a-menu-item key="3">
          <EditFilled />
          <span class="nav-text">My Info</span>
        </a-menu-item>
        
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <!-- Header -->
      <a-layout-header :style="{ background: '#fff', padding: 0 }">
      </a-layout-header>

      <!-- Content -->
      <a-layout-content :style="{ margin: '24px 16px 0' }">
        <!-- registeration zone. new pages that is displaying on the dashboard, has to be
          registered here
        -->
        <router-view 
          v-if="this.$route.path.includes('monitor')"
          :style="{ padding: '24px', minHeight: '83vh'}">
        </router-view>

        <router-view 
          v-else-if="this.$route.path.includes('emergencycontact')"
          :style="{ padding: '24px', minHeight: '83vh'}">
        </router-view>
        <!-- end of registeration zone -->

        <div 
          :style="{ padding: '24px', minHeight: '83vh'}" 
          v-else
        >
          <patients-page v-if="selectedKeys=='1'"/>
          <notification-page v-else-if="selectedKeys=='2'"/>
          <pending-requests-page v-else-if="selectedKeys=='3'"/>
          <my-info-page v-else-if="selectedKeys=='4'"/>
        </div>
      </a-layout-content>

      <!-- Footer -->
      <a-layout-footer style="textAlign: center; bottom:0;">
        Vital Sign Project ©2021 Created by Yizhou Zhao
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>


<script>
// Icons
import { EditFilled, ExclamationCircleFilled, ProfileFilled, PieChartFilled, MailFilled} from '@ant-design/icons-vue';

// Components
import MyInfoPage from './MyInfoPage.vue';
import PatientsPage from './PatientsPage.vue';
import NotificationPage from './NotificationPage.vue';
import PendingRequestsPage from './PendingRequestsPage.vue';
export default {
    name: "Dashboard",

    data() {
        return {
            selectedKeys: ['1'],
        };
    },

    watch:{
      selectedKeys(val){
        this.$store.dispatch('updateDashboardKey', val);
        
        /*
          NOTE: new pages has to be registered here. 
                Otherwise, the page will not be updated when user switching between pages via the sidebar.
        */
        if(this.$route.path.includes('monitor')){
          this.$router.push('/dashboard');
        }

        if(this.$route.path.includes('emergencycontact')){
          this.$router.push('/dashboard');
        }
        
      },
    },

    components: {
        ExclamationCircleFilled,
        PieChartFilled,
        EditFilled,
        MailFilled,
        ProfileFilled,

        MyInfoPage,
        PatientsPage,
        NotificationPage,
        PendingRequestsPage,
        
    },

    mounted(){
        this.selectedKeys = this.$store.getters.dashboardKey;
        
        // redirect user to the login page if the sessionid and csrtoken doesn't exist
        if(this.$getCookie('sessionid') === null
            && this.$getCookie('csrftoken') === null){
            this.$router.push('/');
        }else{
            // if currentUserInfo is empty but the session exists. Get from the server
            this.$get('api/myinfo/')
                .then((response) => {
                    // update user info in the store.
                    this.$store.dispatch('login', response.data)
                      .then(() => {
                        // if current user is a doctor, get his/her patients
                        this.$get('api/patientsof/'+ this.$store.getters.userId +'/')
                          .then((response) => {
                            this.$store.dispatch('addPatients', response.data);
                          }).catch((error) => {
                            console.log(error);
                          });
                        
                        // get a list of pending requests
                        this.$get('api/mypendingrequests/')
                          .then((response) => {
                            this.$store.dispatch('addPendingRequests', response.data);
                          }).catch((error) => {
                            console.log(error);
                          });
                        
                      });
                }).catch((error) =>{
                    // redirect it to the home page if getting error
                    console.log(error);
                    this.$router.push('/');
                });
            
            
        }
        
    },

    methods: {
    onCollapse(collapsed, type) {
    },
    onBreakpoint(broken) {
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