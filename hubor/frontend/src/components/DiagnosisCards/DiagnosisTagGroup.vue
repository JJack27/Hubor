<template>
    <div>
        <template v-for="(tag, index) in tags" :key="index">
            <a-tooltip v-if="tag.length > 20" :title="tag">
              <a-tag :key="tag" :closable="true" @close="handleClose(tag)">
                {{ `${tag.slice(0, 20)}...` }}
              </a-tag>
            </a-tooltip>
            <a-tag v-else :closable="true" @close="handleClose(tag)">
              {{ tag }}
            </a-tag>
        </template>
        <a-auto-complete
            v-if="inputVisible"
            ref="inputRef"
            type="text"
            size="small"
            :style="{ width: '180px' }"
            v-model:value="inputValue"
            @blur="handleInputConfirm"
            @keyup.enter="handleInputConfirm"
            @search="handleSearch"
        >
          <template #dataSource>
            <a-select-option v-for="result in autoResult" :key="result">
              <a-tooltip v-if="result.length > 20" :title="result">
                  {{ `${result.slice(0, 20)}...` }}
              </a-tooltip>
              <div v-else>
                {{ result }}
              </div>
            </a-select-option>
          </template>
        </a-auto-complete>
        <a-tag v-else @click="showInput" style="background: #fff; border-style: dashed">
            <plus-outlined />
            New Diagnosis
        </a-tag>
    </div>
  
</template>
<script>
import { defineComponent, ref, reactive, toRefs, nextTick } from 'vue';
import { PlusOutlined } from '@ant-design/icons-vue';

export default defineComponent({
  name: "DiagnosisTagGroup",
  components: {
    PlusOutlined,
  },
  inject:['id'],

  setup() {
    const inputRef = ref();
    const state = reactive({
      tags: ['High BP', 'Heart Disease'],
      inputVisible: false,
      inputValue: '',
    });

    // load auto-complete options
    const options = reactive([]);
    const autoResult = ref([]);
    const handleSearch = (val) => {
      let resObj = {};
      let res = [];
      resObj = options.value.filter(option => option["DISEASE_NAME"].toLowerCase().includes(val.toLowerCase()));
      for(var i in resObj){
        res.push(resObj[i].DISEASE_NAME);
      }
      
      autoResult.value = res;
    };


    const handleClose = removedTag => {
      // TODO: send DELETE disgnosis/user/diagnosis/
    };

    const showInput = () => {
      state.inputVisible = true;
      nextTick(() => {
        inputRef.value.focus();
      });
    };

    const handleInputConfirm = () => {
      const inputValue = state.inputValue;
      let tags = state.tags;

      if (inputValue && tags.indexOf(inputValue) === -1) {
        tags = [...tags, inputValue];
      }
      Object.assign(state, {
        tags,
        inputVisible: false,
        inputValue: '',
      });
    };

    return { ...toRefs(state), handleClose, showInput, handleInputConfirm, inputRef, options, handleSearch, autoResult };
  },

  mounted(){
    // get all diagnoses options
    this.$get('/api/alldiagnoses/')
      .then(response =>{
        this.options.value = response.data;
      });
  },
});
</script>