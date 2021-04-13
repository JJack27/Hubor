<template>

    <div class="patient-card-list-wrapper">
        <a-card
            class="patient-card-list-wrapper-card"
            :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor, }"
            :hoverable="true"
            :key="item.id"
            v-for="item in this.$store.getters.pendingRequestsArray"
            @click="onClickListItem(item)"
        >
            <a-row>
                <!-- avatar -->
                <a-col :span="2">
                    <a-avatar :src="item.avatar" size="large">
                        <UserOutlined />
                    </a-avatar>
                </a-col>

                <!-- Name and click to know more -->
                <a-col :span="18">
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

                <!-- cancel button -->
                <a-col :span="1" style="padding-top: 8pt!important">
                    <a @click="cancelRequest(item)">cancel</a>
                </a-col>
            </a-row> 
        </a-card>   

        <!-- Modal for canceling the pending request-->
        <a-modal v-model:visible="modalVisible" title="Cancel Request" @ok="handleOk">
            Do you want to cancel the request sent to <span style="font-style: bold">{{ this.selectedItem.owner.first_name + " " + this.selectedItem.owner.last_name}} </span>?
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
            modalVisible: false,
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
        cancelRequest(item){
            this.modalVisible = true;
            this.selectedItem = item;
        },

        handleOk(e){
            console.log(e);
            this.modalVisible = false;
            this.$delete('api/accessrequest/'+this.selectedItem.owner.id+'/'+this.selectedItem.requestor.id+'/')
                .then(response => {
                    this.$message.success("Request canceled!");
                    this.$store.dispatch('removePendingRequests', this.selectedItem.id);
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