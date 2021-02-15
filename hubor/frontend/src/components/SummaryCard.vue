<template>
      <a-card hoverable style="">
        <template #cover>
            <img
                alt="Welcome to the Vital Sign Project"
                :src="require(`@/assets/${this.headerImage}`)"
            />
        </template>
        <a-card-meta :title="this.title" :description="this.detail" style="padding-bottom: 5pt">
            <template #avatar>
                <a-avatar :src="require(`@/assets/${this.avatar}`)" />
            </template>
        </a-card-meta>
    </a-card>
</template>

<script>
export default {
    name:"SummaryCard",
    components:{},
    props:[
        'title',
        'detail',
        'headerImage',
        'avatar'
    ]
}
</script>

<style>
.summary-card-title{
    font-size: 20pt;
}
</style>