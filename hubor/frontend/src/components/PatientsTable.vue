<template>
  <div class='patients-table'>
      <a-row type="flex" justify="start">
          <a-col :span="1" />
          <a-col :span="4">
            <h1>{{this.title}}</h1>
          </a-col>
          <a-col :span="19"/>
      </a-row>
      <a-row type="flex" justify="start">
          <a-col :span="1" />
          <a-col :span="22">
            <a-table :columns="columns" :data-source="this.dataSource"/>
          </a-col>
          <a-col :span="1"/>
      </a-row>
  </div>
</template>

<script>
const columns = [
    {
        dataIndex: 'first_name',
        key: 'first_name',
        title: 'First'
    },
    {
        title: 'Last',
        dataIndex: 'last_name',
        key: 'last_name',
    },
    {
        title: 'Height',
        dataIndex: 'height',
        key: 'height',
    },
    {
        title: 'Weight',
        key: 'weight',
        dataIndex: 'weight'
    },
    {
        title: 'HR',
        key: 'hr',
        dataIndex: 'hr'
    },
    {
        title: 'Temperature',
        key: 'temp',
        dataIndex: 'temp'
    },
    {
        title: 'RR',
        key: 'rr',
        dataIndex: 'rr'
    },
    {
        title: 'SPO2',
        key: 'spo2',
        dataIndex: 'spo2'
    },
  ]
export default {
    name:'PatientsTable',
    props:[
        'title',
        'dataSource'
    ],
    setup(){
        
        return {columns}
    },
    mounted(){
        console.log(this.dataSource)
    }
}
</script>

<style>
.patients-table{
    text-align: left;
    margin-top: 10pt;
}
</style>