<template>
    <div class="pending-request-list-card-wrapper">
        <a-card
            class="pending-request-list-card-wrapper-card"
            title="Pending Requests"
            :headStyle="{background:'#eeeeee', color:'#333333'}"
            :bodyStyle="{background:'#ffffff', color:'#333333'}"
            :hoverable="true"
        >
            <a-list 
                item-layout="horizontal"
                size="large" 
                :pagination="pagination" 
                :data-source="this.$store.getters.pendingRequestsArray"
                class="pending-request-list"
            >
                <template #renderItem="{ item }">
                    <a-list-item key="item.id">
                        <!-- actions -->
                        <template #actions>
                            <a @click="cancelRequest(item)">cancel</a>
                        </template>

                        <!-- metas -->
                        <a-list-item-meta :description="'DoB: ' + item.owner.date_of_birth">
                            <template #title>
                                <a href="#">{{ item.owner.first_name + " " + item.owner.last_name }}</a>
                            </template>
                            <template #avatar>
                                <a-avatar :src="item.owner.avatar" />
                            </template>
                        </a-list-item-meta>

                        <!-- content of the list item, showing when was the request has been sent-->
                        <span class="pending-request-list-item-content" >
                        sent at: {{ new Date(item.time).toDateString() }}
                        </span>
                    </a-list-item>
                </template>
            </a-list>
        </a-card>
        <a-modal v-model:visible="modalVisible" title="Cancel Request" @ok="handleOk">
            Do you want to cancel the request sent to <span style="font-style: bold">{{ this.selectedItem.owner.first_name + " " + this.selectedItem.owner.last_name}} </span>?
        </a-modal>
    </div>
</template>

<script>
export default{
    name: "PendingRequestListCard",
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

.pending-request-list-card-wrapper{
    width:100%;
}

.pending-request-list{
    text-align: start !important;
}

.pending-request-list-item-content{
    text-align: end !important;
    width:50% !important; 
    font-style: italic;
    color:#aaaaaa;
}


</style>