<template>
    <div id="card-body" style="height:100vh; width:25%; background:#444444">
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="8">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="60"
                    unit="rpm"
                    title="RR"
                />
            </a-col>

            <a-col :span="16">
                <VSEntryHorizontal
                    icon="bp_icon.png"
                    value="120/85"
                    unit="mmHg"
                    title="BP"
                />
            </a-col>
        </a-row>

        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <a-col :span="8">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="60"
                    unit="rpm"
                    title="RR"
                />
            </a-col>
            <a-col :span="8">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="60"
                    unit="rpm"
                    title="RR"
                />
            </a-col>
            <a-col :span="8">
                <VSEntryVertical
                    icon="rr_icon.png"
                    :value="60"
                    unit="rpm"
                    title="RR"
                />
            </a-col>
        </a-row>
        
    </div>

</template>

<style>
#card-body .ant-card-bordered{
    border-radius: 10px !important;
}
</style>

<script>
import VSEntryHorizontal  from "../components/PatientStatusEntryCard/VSEntryHorizontal.vue";
import VSEntryVertical  from "../components/PatientStatusEntryCard/VSEntryVertical.vue";
export default {
  name: "Home", 
  components: {
      VSEntryVertical,
      VSEntryHorizontal
  },

  mounted(){
  }
};
</script>