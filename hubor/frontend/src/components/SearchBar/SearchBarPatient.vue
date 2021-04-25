<template>
    <a-auto-complete
            ref="inputRef"
            class="global-search"
            type="text"
            size="large"
            :style="{ width: '80%' }"
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
        </a-auto-complete>
</template>

<script>
import {ref} from 'vue';
export default{
    name:"SearchBarPatient.vue",

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
</style>