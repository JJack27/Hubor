<template>
    <div class="patient-info-cards-group">
        
        <h1 style="font-weight: bold; text-align: start;">
            {{ this.$store.getters.patients[this.$route.params.id].first_name +
            " " + this.$store.getters.patients[this.$route.params.id].last_name}}
        </h1>
        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <!-- Gender -->
            <a-col :span="12">
                <VSEntryVertical
                    :icon="this.$store.getters.patients[this.$route.params.id].gender == 0 ? 'male-icon.png' : 'female-icon.png' "
                    :value="this.$store.getters.patients[this.$route.params.id].gender == 0 ? 'Male' : 'Female' "
                    unit=" "
                    title="Gender"
                />
            </a-col>

            <!-- date of birth -->
            <a-col :span="12">
                <VSEntryVertical
                    icon="calendar-icon.png"
                    :value="this.$store.getters.patients[this.$route.params.id].date_of_birth"
                    unit=" "
                    title="Date of Birth"
                />
            </a-col>
        </a-row>

        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <!-- Medication -->
            <a-col :span="24">
                <medication-card-vertical />
            </a-col>
        </a-row>

        <a-row type="flex" justify="bottom" :gutter="[16,16]">
            <!-- Diagnosis -->
            <a-col :span="24">
                <diagnosis-card-vertical />
            </a-col>
        </a-row>

    </div>

</template>

<script>

import {PhoneFilled, HomeFilled} from '@ant-design/icons-vue';
import VSEntryVertical from './VSEntryCard/VSEntryVertical.vue';
import VSEntryHorizontal from './VSEntryCard/VSEntryHorizontal.vue';
import MedicationCardHorizontal from './MedicationCards/MedicationCardHorizontal.vue';
import MedicationCardVertical from './MedicationCards/MedicationCardVertical.vue';
import DiagnosisCardVertical from './DiagnosisCards/DiagnosisCardVertical.vue';

export default{
    name: "PatienInfoCardsGroup",

    components:{
        PhoneFilled,
        HomeFilled,
        VSEntryVertical,
        VSEntryHorizontal,
        MedicationCardHorizontal,
        MedicationCardVertical,
        DiagnosisCardVertical,
    },

    data(){
        return {
            id: this.$route.params.id,
        }
    },
    watch:{
        id(newv, oldv){
            this.$forceUpdate();
            console.log(newv);
        }
    },

    methods:{
    },

    setup() {
      return {
        emergency_contacts_columns: [
                {
                    title: 'First Name',
                    dataIndex: 'first_name',
                    key: 'first_name',
                },
                {
                    title: 'Last Name',
                    dataIndex: 'last_name',
                    key: 'last_name',
                },
                {
                    title: 'Phone',
                    dataIndex: 'phone',
                    key: 'phone',
                },
                {
                    title: 'Email',
                    dataIndex: 'email',
                    key: 'email',
                },
            ]
      };
    },


}
</script>

<style>
.patient-info-cards-group .ant-card-bordered{
    border-radius: 10px !important;
    text-align: start !important;
}
</style>