<template>
    <div>
        <a-card
            :hoverable="false"
            style="border-radius: 10px !important; background:#fff; color:#918de0; text-align:start !important; height:100% !important; margin-top:10pt;"
            @click="activate"
            
        >   
            <template v-slot:title>
                <a-row>
                
                    <span style="font-size:12pt; font-weight:bold;" > {{this.item.first_name +' '+ this.item.last_name}} </span>
                    <span style="font-style:italic; font-size:10pt; padding-left:8px; padding-right:10px; 
                        background:#918de0; border-radius:25px; padding-top:1px; padding-bottom:-5px;
                        color:#fff; text-transform: capitalize; margin-left:10pt;"> 
                        {{item.relationship}} 
                    </span>
                </a-row> 
            </template>
            
            
            <!-- phone -->
            <a-row type="flex" align="middle" :gutter="[16,16]">
                <a-col :span="1">
                    <i class="fa fa-phone" aria-hidden="true"></i>
                </a-col>
                <a-col :span="18" style="text-align: start; ">
                    <!-- style="padding-left:5px; padding-right:5px; border:1px solid; border-radius:25px; padding-top:2px; padding-bottom:2px;" -->
                    <a :href="'callto:'+item.phone" >{{item.phone}}</a>
                </a-col>
            </a-row>

            <!-- email -->
            <a-row type="flex" align="middle" :gutter="[16,16]">
                <a-col :span="1">
                    <i class="fa fa-envelope" aria-hidden="true"></i>
                </a-col>
                <a-col :span="18" style="text-align: start; ">
                    <a :href="'mailto:'+item.email">{{item.email}}</a>
                </a-col>
            </a-row>

        </a-card>
    </div>
</template>

<script>
export default{
    name: "EMContactInformationCard",
    props:[
        'item',
    ],

    methods:{
        activate(){
            window.location.href = this.href;
        }
    }
    
}
</script>

<style>
</style>