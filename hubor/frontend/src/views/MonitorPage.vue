<template>
    <div>
        <div style="width:100%; text-align:start">
            <ArrowLeftOutlined @click="backToDashboard"/>
        </div>
        
        <a-tabs v-model:activeKey="activeKey">
        <a-tab-pane key="1" tab="Now">
          <PatientNowPage
          />
        </a-tab-pane>
        <a-tab-pane key="2" tab="History">
          <PatientHistoryPage
          />
        </a-tab-pane>
        
      </a-tabs>
    </div>
</template>

<script>
import {ArrowLeftOutlined} from "@ant-design/icons-vue";
import PatientNowPage from "./PatientNowPage.vue";
import PatientHistoryPage from "./PatientHistoryPage.vue";

export default{
    name:"MonitorPage",
    components:{
        ArrowLeftOutlined,
        PatientHistoryPage,
        PatientNowPage,
    },
    
    props:[
        
    ],

    methods:{
        backToDashboard(){
            this.$router.push("/dashboard");
        }
    }

}
</script>

<style>
</style>