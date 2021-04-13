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
        <a-input
            v-if="inputVisible"
            ref="inputRef"
            type="text"
            size="small"
            :style="{ width: '78px' }"
            v-model:value="inputValue"
            @blur="handleInputConfirm"
            @keyup.enter="handleInputConfirm"
        />
        <a-tag v-else @click="showInput" style="background: #fff; border-style: dashed">
            <plus-outlined />
            New Medicine
        </a-tag>
    </div>
  
</template>
<script>
import { defineComponent, ref, reactive, toRefs, nextTick } from 'vue';
import { PlusOutlined } from '@ant-design/icons-vue';
export default defineComponent({
  name: "MedicationTagGroup",
  components: {
    PlusOutlined,
  },
  inject:['id'],

  setup() {
    const inputRef = ref();
    const state = reactive({
      tags: ['Tylenol', 'Aspring', 'Aptiom'],
      inputVisible: false,
      inputValue: '',
    });

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
    };

    return { ...toRefs(state), handleClose, showInput, handleInputConfirm, inputRef };
  },
});
</script>