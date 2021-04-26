<template>
    <div>
        <a-card
            class="vs-entry-wrapper-card"
            :bodyStyle="{background:this.bodyBackColor, color:this.BodyFontColor}"
            :hoverable="true"
            @click="showModal"
        >
            <a-row type="flex" justify="center" align="bottom">
                <a-col :span="4">
                    <img
                        :src="require(`@/assets/icons/${this.icon}`)"
                        height="30"
                        width="30"
                        class="list-item-icon">
                </a-col>
                <a-col :span="20" class="vs-title">
                    <span v-html="this.title"></span>
                </a-col>
                
            </a-row>
            <a-row type="flex" justify="center" align="bottom">
                <a-col class="vs-data" :span="11">
                    <a-row type="flex" justify="space-between">
                        <a-col :span="6">
                            <div style="font-size:8pt; text-align:start">MIN</div>
                            {{ this.diastolicLow }}
                        </a-col>
                        <a-col :span="11" style="text-align:center">
                            <a-divider style="color: #aaa; font-size:9pt; font-style:italic">DBP</a-divider>
                        </a-col>
                        <a-col :span="6" style="text-align:end;">
                            <div style="font-size:8pt; text-align:end">MAX</div>
                            {{ this.diastolicHigh }}
                        </a-col>
                    </a-row>
                </a-col>
                <a-col class="vs-data" :span="2" style="text-align:center">
                    <a-divider type="vertical" style="height: 30pt; background-color: #918de0"/>
                </a-col>
                <a-col class="vs-data" :span="11">
                    <a-row type="flex" justify="space-between" algin="bottom">
                        <a-col :span="6">
                            <div style="font-size:8pt; text-align:start">MIN</div>
                            {{ this.systolicLow }}
                        </a-col>
                        <a-col :span="10">
                            <a-divider style="color: #aaaaaa; font-size:9pt; font-style:italic">SBP</a-divider>
                        </a-col>
                        <a-col :span="6" style="text-align:end;">
                            <div style="font-size:8pt; text-align:end">MAX</div>
                            {{ this.systolicHigh }}
                        </a-col>
                    </a-row>
                </a-col>
            </a-row>
        </a-card>

        <!-- Modal and form for updating normal range -->
        <a-modal 
            v-model:visible="normalRangeVisiable" 
            :title="'Edit ' + this.title + ' Ranges'" 
            :footer="null"
            :closable="true"
        >
            <a-row style="width=40%!important">
                <a-col :span="10">
                    <a-input
                        v-model:value="this.ll"
                    />
                </a-col>
                <a-col :span="4" style="text-align:center">
                - Diastolic -
                </a-col>
                <a-col :span="10">
                    <a-input
                        v-model:value="this.lh"
                    />
                </a-col>
            </a-row>
            <a-row style="width=40%!important">
                <a-col :span="10">
                    <a-input
                        v-model:value="this.hl"
                    />
                </a-col>
                <a-col :span="4" style="text-align:center">
                - Systolic -
                </a-col>
                <a-col :span="10">
                    <a-input
                        v-model:value="this.hh"
                    />
                </a-col>
            </a-row>
            <br/>
            <a-row style="width=40%!important" >
                <a-col :span="17"></a-col>
                <a-col :span="3" style="text-algin:end">
                    <a-button 
                        type="primary"
                        @click="saveChange"
                    >
                        Save
                    </a-button>
                </a-col>
                <a-col :span="1"></a-col>
                <a-col :span="3" style="text-algin:end">
                    <a-button 
                        type="bordered"
                        @click="closeModal"
                    >
                        Cancel
                    </a-button>
                </a-col>
                
            </a-row>
        </a-modal>
    </div>
    
</template>

<script>
export default {
    name: "NormalRangeCard",
    props: ['icon', 'diastolicLow', 'diastolicHigh', 'systolicLow', 'systolicHigh', 'background', 'color', 'title'],
    inject:['id'],
    emit:['save-normal-range'],
    data(){
        return {
            normalRangeVisiable: false,
            hl: 0,
            ll: 0,
            hh: 0,
            lh: 0,
            id: this.$route.params.id,
        }
    },

    mounted(){
        this.ll = this.diastolicLow;
        this.lh = this.diastolicHigh;
        this.hl = this.systolicLow;
        this.hh = this.systolicHigh;
    },

    methods:{
        showModal(){
            this.normalRangeVisiable = true;
        },

        closeModal(){
            this.normalRangeVisiable = false;
        },

        saveChange(){
            // TODO: send request to the server
            var state = {};
            state['bpl_l'] = this.ll;
            state['bpl_h'] = this.lh;
            state['bph_l'] = this.hl;
            state['bph_h'] = this.hh;
            this.$put(`/api/normalrange/${this.$route.params.id}/bpl_l/`, {"value": this.ll})
            .then((response) =>{
                this.$put(`/api/normalrange/${this.$route.params.id}/bpl_h/`, {"value": this.lh})
                .then((response)=>{
                    this.$put(`/api/normalrange/${this.$route.params.id}/bph_h/`, {"value": this.hh})
                    .then((response) =>{
                        this.$put(`/api/normalrange/${this.$route.params.id}/bph_l/`, {"value": this.hl})
                        .then(response =>{
                            this.$message.success("Updating normal range is successful");
                            this.$emit('save-normal-range', state);
                            this.normalRangeVisiable = false;
                        })
                        .catch((error) =>{
                            this.$message.error("Updating normal range is unsuccessful")
                        });
                    })
                })
                
            })
            .catch((error) =>{
                this.$message.error("Updating normal range is unsuccessful")
            });
        }
    }
}


</script>

<style>
.vs-data{
    font-size: 22pt;
    font-weight:bold;
    color: #0a0956;
    margin-top:10px;
    padding-top: 10px;
    text-align:start;
}

.vs-unit{
    font-size: 8pt;
    text-align: end !important;
    font-weight: bold;
    padding-bottom: 13px !important;
}

.vs-title{
    font-size: 12pt;
    text-align: end;
    color: #aaaaaa;
    font-weight:bold;
}

.vs-entry-wrapper-card{
    text-align: start;
}

.vs-entry-wrapper-card .ant-card-body{
    padding-top: 12px;
    padding-bottom: 12px;
}
</style>