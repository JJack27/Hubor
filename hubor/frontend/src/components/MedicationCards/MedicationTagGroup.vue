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
            @select="handleSelect"
        >
          <template #dataSource>
            <a-select-option v-for="result in autoResult" :key="result">
              <p style="font-weight:bold; font-size:11pt;">{{result.GENERIC_NAME}}</p>
              <p style="font-style:italic; font-size:8pt; padding:0;">{{result.BRAND_NAMES}}</p>
            </a-select-option>
          </template>
        </a-auto-complete>
        <a-tag v-else @click="showInput" style="background: #fff; border-style: dashed">
            <plus-outlined />
            New Medication
        </a-tag>
    </div>
  
</template>
<script>
import { defineComponent, ref, reactive, toRefs, nextTick } from 'vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { useRoute } from 'vue-router';
export default defineComponent({
  name: "MedicationTagGroup",
  components: {
    PlusOutlined,
  },
  data(){
    return{
      id: this.$route.params.id,
    }
  },

  setup() {
    const inputRef = ref();
    const state = reactive({
      tags: ['Tylenol', 'Aspring', 'Aptiom'],
      inputVisible: false,
      inputValue: '',
    });
    const route = useRoute();
    const id = route.params.id;
    
    const handleClose = removedTag => {
      // TODO: send DELETE /prescription/user/medication/

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
    }

    // load auto-complete options
    const options = reactive([]);
    const autoResult = ref([]);

    const handleSearch = (val) => {
      let resObj = {};
      // will filter by both GENERIC_NAME and BRAND_NAMES
      resObj = options.value.filter(option => option["BRAND_NAMES"].toLowerCase().includes(val.toLowerCase()) 
              || option["GENERIC_NAME"].toLowerCase().includes(val.toLowerCase()) 
      );
      autoResult.value = resObj;
    };
    // only display GENERIC_NAME when user select an option
    const handleSelect = (val, option) =>{
      state.inputValue = val.GENERIC_NAME;
      handleInputConfirm();
    };

    return { ...toRefs(state), handleClose, showInput, handleInputConfirm, inputRef, options, autoResult, handleSearch, handleSelect };
  },

  mounted(){
    // get all diagnoses options
    this.$get('/api/allmedicines/')
      .then(response =>{
        this.options.value = response.data;
      });
  },
});
</script>