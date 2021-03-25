<template>
    <div class="patient-card-list-wrapper">
        <a-card
            class="patient-card-list-wrapper-card"
            :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor, }"
            :hoverable="true"
            :key="item.id"
            v-for="item in this.dataSource"
            @click="onClickListItem(item)"
        >
            <a-row>
                <!-- avatar -->
                <a-col :span="2">
                    <a-badge dot :status="this.status">
                        <a-avatar :src="item.avatar" size="large">
                            <UserOutlined />
                        </a-avatar>
                    </a-badge>
                </a-col>

                <!-- Name and click to know more -->
                <a-col :span="21">
                    <h4>{{item.first_name + " " + item.last_name}}</h4>
                    <br>
                    <p style="margin-top: -25pt !important">Click to know more</p>
                </a-col>

                <!-- right triangle -->
                <a-col :span="1" style="padding-top: 8pt!important">
                    <a >▶</a>
                </a-col>
            </a-row> 
        </a-card>
        
    </div>
</template>

<script>
import {UserOutlined} from '@ant-design/icons-vue';
export default{
    name: "PaitentCardList",
    components:{
        UserOutlined,
    },
    props:[
        'title',
        'status',
        'dataSource',
        'headerBackColor',
        'headerFontColor',
        'bodyBackColor',
        'BodyFontColor'
    ],

    setup(){
        const pagination = {
            pageSize: 3,
        };

        return {
            pagination,
        }
    },

    mounted(){
    },

    methods :{
        onClickListItem(item){
            this.$router.push('/dashboard/monitor/'+item.id);
        },
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