<template>
    <div>
        <a-card
            :hoverable="true"
            style="border-radius: 10px !important; background:#fff; color:#918de0; text-align:center !important; height:100% !important;"
            @click="activate"
        >
            <a-row type="flex" align="middle">
                <a-col :span="4">
                    <i :class="this.icon" aria-hidden="true" style="font-size: 30pt;"></i>
                </a-col>
                <a-col :span="18" style="text-align: end; ">
                    <a :href="this.href">{{this.content}}</a>
                </a-col>
            </a-row>
        </a-card>
    </div>
</template>

<script>
export default{
    name: "ContactInformationCard",
    inject:['id'],
    props:[
        'icon',
        'content',
        'href',
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