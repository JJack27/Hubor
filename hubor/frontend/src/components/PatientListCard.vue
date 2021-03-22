<template>
    <div class="patient-list-card-wrapper">
        <a-card
            class="patient-list-card-wrapper-card"
            :title="this.title"
            :headStyle="{background:this.headerBackColor, color:this.headerFontColor}"
            :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor, }"
            :hoverable="false"
        >
            <a-list 
                item-layout="horizontal"
                size="large" 
                :pagination="pagination" 
                :data-source="this.dataSource"
                class="patient-list"
            >
                <template #renderItem="{ item }">
                    <a-list-item key="item.id">
                        <!-- actions -->
                        <template #actions>
                            <a :href="'monitor/'+item.id">monitor</a>
                        </template>

                        <!-- metas -->
                        <a-list-item-meta :description="item.date_of_birth">
                            <template #title>
                                <a :href="'monitor/'+item.id">{{ item.first_name + " " + item.last_name }}</a>
                            </template>
                            <template #avatar>
                                <a-avatar :src="item.avatar" />
                            </template>
                        </a-list-item-meta>
                        <!-- content of the list item, showing the HR, RR, SPO2, TEMP-->
                        <a-row style="width:80% !important">
                            <a-col :span="2" >
                                <p style="padding-top:8pt!important;">
                                    <i class="fa fa-arrows-v" aria-hidden="false"></i><sp/><sp/>   {{item.height}} KG 
                                    <br> 
                                    <i class="fa fa-arrows-h" aria-hidden="true"></i> {{item.weight}} CM 
                                </p>
                            </a-col>
                            <a-col :span="6" >
                                <p style="padding-top:8pt!important;">
                                    <i class="fa fa-phone-square" aria-hidden="true"></i> {{item.phone}} 
                                    <br> 
                                    <i class="fa fa-envelope" aria-hidden="true"></i> {{item.email}} 
                                </p>
                            </a-col>
                            <a-col :span="4">
                                <PatientListVitalSignEntry
                                    icon="hr_icon.png"
                                    :value="item.hr"
                                    unit="bpm"
                                />
                            </a-col>
                            <a-col :span="4">
                                <PatientListVitalSignEntry
                                    icon="rr_icon.png"
                                    :value="item.rr"
                                    unit="rpm"
                                />
                            </a-col>
                            <a-col :span="4">
                                <PatientListVitalSignEntry
                                    icon="spo2_icon.png"
                                    :value="item.spo2"
                                    unit="%"
                                />
                            </a-col>
                            <a-col :span="4">
                                <PatientListVitalSignEntry
                                    icon="temp_icon.png"
                                    :value="item.temp"
                                    unit="°C"
                                />
                            </a-col>
                        </a-row>
                    </a-list-item>
                </template>
            </a-list>
        </a-card>
        
    </div>
</template>

<script>
import PatientListVitalSignEntry from '../components/PatientListVitalSignEntry.vue';
export default{
    name: "PatientListCard",
    components:{
        PatientListVitalSignEntry,
    },
    props:[
        'title',
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
        onClickListItem(id){
            console.log(id);
        },
    }
}
</script>

<style>
.patient-list-card-wrapper{
    width:100%;
}

.patient-list{
    text-align: start !important;
}

.list-item-icon{
    margin-top:8px;
}


</style>