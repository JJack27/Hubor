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
                <a-col class="vs-data" :span="24">
                    <a-row type="flex" justify="space-between">
                        <a-col :span="10">
                            <div style="font-size:8pt; text-align:start">MIN</div>
                            {{ this.low }}
                        </a-col>
                        <a-col :span="10" style="text-align:end;">
                            <div style="font-size:8pt; text-align:end">MAX</div>
                            {{ this.high }}
                        </a-col>
                    </a-row>
                </a-col>
            </a-row>
        </a-card>

        <a-modal 
            v-model:visible="normalRangeVisiable" 
            :footer="null"
            :closable="true"
        >
            <template v-slot:title>
                <span v-html="'Edit ' + this.title + ' Ranges'" ></span>
            </template>
            <a-row style="width=40%!important">
                <a-col :span="10">
                    <a-input
                        v-model:value="this.l"
                    />
                </a-col>
                <a-col :span="4" style="text-align:center">
                -
                </a-col>
                <a-col :span="10">
                    <a-input
                        v-model:value="this.h"
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
    name: "BPNormalRangeCard",
    // prefix: one of ['hr', 'rr', 'spo2', 'bp', 'temp']
    props: ['icon', 'low', 'high', 'background', 'color', 'title', 'prefix'],
    emit:['save-normal-range'],
    data(){
        return {
            normalRangeVisiable: false,
            h: 0,
            l: 0,
            id: this.$route.params.id,
        }
    },

    mounted(){
        this.h = this.high;
        this.l = this.low;
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
            state[this.prefix + '_l'] = this.l;
            state[this.prefix + '_h'] = this.h;
            this.$put(`/api/normalrange/${this.$route.params.id}/${this.prefix + '_l'}/`, {"value": this.l})
            .then((response) =>{
                this.$put(`/api/normalrange/${this.$route.params.id}/${this.prefix + '_h'}/`, {"value": this.h})
                .then((response)=>{
                    this.$message.success("Updating normal range is successful");
                    this.$emit('save-normal-range', state);
                    this.normalRangeVisiable = false;
                })
                .catch((error) =>{
                    this.$message.error("Updating normal range is unsuccessful")
                });
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