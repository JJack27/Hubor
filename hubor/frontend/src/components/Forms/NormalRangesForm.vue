<template>
  <a-form
    id='add-patient-form'
    ref="formRef"
    :model="formState"
    :rules="rules"
    v-bind="layout"
  > 
    <!-- HR -->
    <a-row>
      <a-col :span="12">
        <a-form-item required  label="HR High" name="hr_h">
          <a-input placeholder="120" type="number" v-model:value="formState.hr_h" autocomplete="off" />
        </a-form-item>
      </a-col>

      <a-col :span="12">
        <a-form-item required  label="HR Low" name="hr_l">
          <a-input placeholder="40" type="number" v-model:value="formState.hr_l" autocomplete="off" />
        </a-form-item>
      </a-col>
    </a-row>

    <!-- RR -->
    <a-row>
      <a-col :span="12">
        <a-form-item required  label="RR High" name="rr_h">
          <a-input placeholder="70" type="number" v-model:value="formState.rr_h" autocomplete="off" />
        </a-form-item>
      </a-col>

      <a-col :span="12">
        <a-form-item required  label="RR Low" name="rr_l">
          <a-input placeholder="40" type="number" v-model:value="formState.rr_l" autocomplete="off" />
        </a-form-item>
      </a-col>
    </a-row>

    <!-- TEMP -->
    <a-row>
      <a-col :span="12">
        <a-form-item required  label="TEMP High" name="temp_h">
          <a-input placeholder="37.5" type="number" v-model:value="formState.temp_h" autocomplete="off" />
        </a-form-item>
      </a-col>

      <a-col :span="12">
        <a-form-item required  label="TEMP Low" name="temp_l">
          <a-input placeholder="36" type="number" v-model:value="formState.temp_l" autocomplete="off" />
        </a-form-item>
      </a-col>
    </a-row>

    <!-- SPO2 -->
    <a-row>
      <a-col :span="12">
        <a-form-item required  label="SPO2 High" name="spo2_h">
          <a-input placeholder="100" type="number" v-model:value="formState.spo2_h" autocomplete="off" />
        </a-form-item>
      </a-col>

      <a-col :span="12">
        <a-form-item required  label="SPO2 Low" name="spo2_l">
          <a-input placeholder="90" type="number" v-model:value="formState.spo2_l" autocomplete="off" />
        </a-form-item>
      </a-col>
    </a-row>

    <!-- BP -->
    <a-row>
      <a-col :span="12">
        <a-form-item required  label="BP High" name="bp_h">
          <a-input placeholder="130" type="number" v-model:value="formState.bp_h" autocomplete="off" />
        </a-form-item>
      </a-col>

      <a-col :span="12">
        <a-form-item required  label="BP Low" name="bp_l">
          <a-input placeholder="80" type="number" v-model:value="formState.bp_l" autocomplete="off" />
        </a-form-item>
      </a-col>
    </a-row>
  

    <a-form-item>
      <a-button type="primary" @click="onSubmit">Submit</a-button>
      <a-button style="margin-left: 10px" @click="resetForm">Reset</a-button>
      <a-button style="margin-left: 10px" @click="cancelForm">Cancel</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import { defineComponent, reactive, ref, toRaw, inject, readonly} from 'vue';
import Axios from 'axios';
export default defineComponent({
    name:"NormalRangesForm",
    emits:['edited-normal-ranges'],
    inject:[
      'id',
      'ranges',
    ],


    setup: () => {
        const formRef = ref();
        const formState = inject('ranges');
        const initState = readonly('ranges');

        const layout = {
          labelCol: {
              span: 8,
          },
          wrapperCol: {
                span: 14,
            },
        };

        const resetForm = () => {
          formState = initState;
        };

        return {
          formState,
          formRef,
          resetForm,
          initState,
        };
    },
    /// end of setup()

    methods: {
        onSubmit(){
          // TODO: send request to edit normal ranges
          var rawState = toRaw(this.formState);
          this.$emit("edited-normal-ranges", rawState);
        }, 

        cancelForm(){
          var rawState = toRaw(this.initState);
          this.$emit("edited-normal-ranges", rawState);
        },

    },

    /*
    mounted(){
      this.formState = initState;
    };
    */

});
</script>

<style>
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}

#add-patient-form .ant-form-item{
    margin-bottom: 12px;
}
</style>