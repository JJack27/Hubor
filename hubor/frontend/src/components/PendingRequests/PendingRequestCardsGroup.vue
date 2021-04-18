<template>

    <div class="patient-card-list-wrapper">
        <a-card
            class="patient-card-list-wrapper-card"
            :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor, }"
            :hoverable="false"
            :key="item.id"
            v-for="item in this.$store.getters.pendingRequestsArray"
        >
            <a-row>
                <!-- avatar -->
                <a-col :span="2">
                    <a-avatar :src="item.avatar" size="large">
                        <UserOutlined />
                    </a-avatar>
                </a-col>

                <!-- Name and click to know more -->
                <a-col :span="17">
                    <h4>{{item.owner.first_name + " " + item.owner.last_name}}</h4>
                    <br>
                    <p style="margin-top: -25pt !important">{{ 'DoB: ' + item.owner.date_of_birth }}</p>
                </a-col>

                <!-- Sent at -->
                <a-col :span="3" style="padding-top: 8pt!important">
                    <span class="pending-request-list-item-content" >
                        sent at: {{ new Date(item.time).toDateString() }}
                    </span>
                </a-col>

                <!-- accept button -->
                <a-col :span="1" style="padding-top: 8pt!important">
                    <a @click="acceptRequest(item)">accept</a>
                </a-col>

                <!-- deny button -->
                <a-col :span="1" style="padding-top: 8pt!important">
                    <a @click="denyRequest(item)">deny</a>
                </a-col>
            </a-row> 
        </a-card>   

        <!-- Modal for accepting the pending request-->
        <a-modal v-model:visible="acceptModalVisible" title="Accept the Request" @ok="handleAcceptOk">
            Do you want to accept the request from <span style="font-style: bold">{{ this.selectedItem.owner.first_name + " " + this.selectedItem.owner.last_name}} </span>?
        </a-modal>

        <!-- Modal for denying the pending request-->
        <a-modal v-model:visible="denyModalVisible" title="Deny the Request" @ok="handleDenyOk">
            Do you want to deny the request from <span style="font-style: bold">{{ this.selectedItem.owner.first_name + " " + this.selectedItem.owner.last_name}} </span>?
        </a-modal>
    </div>
</template>

<script>
import {UserOutlined} from '@ant-design/icons-vue';
export default{
    name: "PendingRequestCardsGroup",
    components:{
        UserOutlined,
    },

    setup(){
        const pagination = {
            pageSize: 3,
        };

        return {
            pagination,
        }
    },

    data(){
        return{
            denyModalVisible: false,
            acceptModalVisible: false,
            selectedItem:{
                owner:{
                    first_name: null,
                    last_name: null,
                }
            },
        }
    },

    mounted(){
        this.$get('api/mypendingrequests/')
            .then(response => {
                this.$store.dispatch('addPendingRequests', response.data);
            })
    },

    methods:{
        denyRequest(item){
            this.denyModalVisible = true;
            this.selectedItem = item;
        },

        handleDenyOk(e){
            console.log(e);
            this.denyModalVisible = false;
            this.$delete('api/accessrequest/'+this.selectedItem.owner.id+'/'+this.selectedItem.requestor.id+'/')
                .then(response => {
                    this.$message.success("Request canceled!");
                    this.$store.dispatch('removePendingRequests', this.selectedItem.id);
                }).catch(err => {
                    this.$message.error("Request not canceled!");
                })
        },

        acceptRequest(item){
            this.acceptModalVisible = true;
            this.selectedItem = item;
        },

        handleAcceptOk(e){
            console.log(e);
            this.acceptModalVisible = false;
            this.$post('api/accessrequest/'+this.selectedItem.owner.id+'/'+this.selectedItem.requestor.id+'/')
                .then(response => {
                    this.$message.success("Request accepted!");
                    this.$store.dispatch('removePendingRequests', this.selectedItem.id);
                    // fetch the newest patient information
                    this.$get(`api/patientsof/${this.$store.getters.userId}/`)
                        .then(response => {
                            this.$store.dispatch('addPatients', response.data);
                        });
                }).catch(err => {
                    this.$message.error("Request not canceled!");
                })
        }
    }
}
</script>

<style>
.patient-card-list-wrapper{
    margin-top:-10pt!important;
    width:100%;
}

.patient-card-list-wrapper-card{
    margin-top: 10pt !important;
    text-align: start !important;
    
}

.patient-card-list-wrapper-card .ant-card-body{
    padding-bottom: 4pt !important;
}


.patient-card-list-wrapper-card .ant-card{
    
}

.list-item-icon{
    margin-top:8px;
}

</style>