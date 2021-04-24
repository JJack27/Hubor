<template>
    <div>
        <div style="width:100%; text-align:start">
            <ArrowLeftOutlined @click="backToDashboard" height="2em"/>
        </div>
        
        <a-tabs v-model:activeKey="activeKey">
        <a-tab-pane key="1" tab="Now">
          <PatientNowPage
            @switch-to-history="handleSwitch"
          />
        </a-tab-pane>
        <a-tab-pane key="2" tab="History">
          <PatientHistoryPage
            :vsProp="this.vs"
            :titleProp="this.title"
          />
        </a-tab-pane>
        
      </a-tabs>
    </div>
</template>

<script>
import {ArrowLeftOutlined} from "@ant-design/icons-vue";
import PatientNowPage from "./PatientNowPage.vue";
import PatientHistoryPage from "./PatientHistoryPage.vue";
const map={
    "hr": "heart rate",
    "rr": "respiration rate",
    "spo2": `O${"2".sub()} Saturation`,
    "temp": "temperature"
}
export default{
    name:"MonitorPage",
    components:{
        ArrowLeftOutlined,
        PatientHistoryPage,
        PatientNowPage,
    },
    data(){
        return{
            activeKey: '1',
            vs: 'hr',
            title: "heart rate",
        }
    },
    
    provide(){
        return{
            'id': this.$route.params.id
        }
    },
    watch:{
        vs: function(newVal, oldVal){
            this.title = map[newVal];
        }
    },
    methods:{
        backToDashboard(){
            this.$router.push("/dashboard");
        },
        // method to handle event when user click on now-status-card
        // switch to history
        handleSwitch(vs){
            // switch to history key
            this.activeKey = '2';
            this.vs = vs;
            console.log("monitor", this.vs)
        },
    }

}
</script>

<style>
</style>