<template>
  <div id="search-bar">
    <a-auto-complete
            ref="inputRef"
            type="text"
            size="large"
            :style="{ width: '95%' }"
            v-model:value="inputValue"
            @select="handleSelect"
            @search="handleSearch"
            @blur="handleBlur"
        >
          <template #dataSource>
            <a-select-option v-for="patient in searchResult" :key="patient">
              <div>
                {{ patient.first_name }} {{ patient.last_name }}
              </div>
            </a-select-option>
          </template>
          <a-input v-model:value="inputValue" placeholder="Search...">
            <template #prefix><SearchOutlined :style="{fontSize: '16px', color: '#555'}"/></template>
          </a-input>
    </a-auto-complete>
  </div>
</template>

<script>
import {ref} from 'vue';
import {SearchOutlined } from '@ant-design/icons-vue';
export default{
    name:"SearchBarPatient.vue",
    components:{
      SearchOutlined,
    },
    setup(){
        // search bar
        const inputRef = ref();
        const inputValue = ref('');
        const searchResult = ref([]);

        return{
            inputRef, inputValue, searchResult
        }
    },

    methods:{
        handleSearch(query){
            let res = [];
            // will filter by both last_name, first_name and first_name + last_name
            res = this.$store.getters.patientsArray.filter(patient => patient["first_name"].toLowerCase().includes(query.toLowerCase()) 
                    || patient["last_name"].toLowerCase().includes(query.toLowerCase()) 
                    || (`${patient['first_name']} ${patient['last_name']}`).toLowerCase().includes(query.toLowerCase()) 
            );
            this.searchResult = res;
        },

        handleSelect(val, option){
            this.inputValue = '';
            this.$router.push(`/dashboard/monitor/${val.id}`);
            this.$forceUpdate()
            val = ""
        },

        handleBlur(){
            this.inputValue = "";
        }
    }

}
</script>

<style>
#search-bar .ant-input {
	border-radius: 90px !important;
	
  border: 0;
}

#search-bar .ant-input-affix-wrapper{
  border-radius: 90px !important;
  border:0;
}
</style>