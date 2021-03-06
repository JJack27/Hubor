<template>
    <div>
        <a-row type="flex" justify="center" align="middle" :gutter="[16,16]">
                
            <a-col :span="9" style="text-align:end">
                <img
                    :src="require(`@/assets/icons/${this.vs}_icon.png`)"
                    height="20"
                    width="20"
                    style="margin-top:-7pt;"
                >
            </a-col>
            <a-col :span="10" style="text-align:start">
                <h1 style="text-transform: capitalize;"> <span v-html="this.title"></span> </h1>
            </a-col>

            <a-col :span="5" style="text-align:end">
                <h1> {{this.date}} </h1>
            </a-col>
        </a-row>

            <div style="text-align:end">
                <a-row type="flex" justify="end">
                    <a-col :span="1">
                        <a-switch size="small" v-model:checked="showMinMax" @click="$forceUpdate"/>
                    </a-col>
                    <a-col :span="2">
                        Min-Max
                    </a-col>
                </a-row>

                <a-row type="flex" justify="end">
                    <a-col :span="1">
                        <a-switch size="small" v-model:checked="showStdev" @click="$forceUpdate"/>
                    </a-col>
                    <a-col :span="2">
                        Variance
                    </a-col>
                </a-row>

                <a-row type="flex" justify="end">
                    <a-col :span="1">
                        <a-switch size="small" v-model:checked="showAbnormal" @click="$forceUpdate"/>
                    </a-col>
                    <a-col :span="2">
                        Abnormal
                    </a-col>
                </a-row>
                
            </div>
            <div id="container">
            </div>
        
    </div>
</template>

<script>
import { defineComponent, ref, inject } from 'vue';
import { MultiView } from '@antv/g2plot';

export default defineComponent({
    name:"VSAreaChart",
    props:[
        'vsData',
        'vs',    // hr, rr, spo2...
        'stat',     // mean, max, min, median, stdev
        'timeSpan', // min, hr, day, 
        'title'  
    ],
    data(){
        return{
            aType: "min",
            toTime: null,
            fromTime: null,
            chart: null,
            dataDisplay: [],
            dataRange: [],
            dataStdev: [],
            valueMin: 10000,
            valueMax: -10000,
            showMinMax: false,
            showStdev: false,
            showAbnormal: false,
            date: "",
            showChart: true,
            id: this.$route.params.id,
        }
    },

    computed:{
        now(){
            return new Date().toJSON();
        },

        oneHrBeforeNow(){
            var now = new Date()
            var oneHr = 3600000;
            var anHrBeforeNow = new Date(now - oneHr);
            return anHrBeforeNow.toJSON();
        }

    },
    beforeUnmount(){
        this.chart.destroy();
    },

    updated(){
        // update DataDisplay
        this.dataDisplay = []
        var views = [];
        var annotations = [];
        var vs = this.vs;
        
        
        this.date = new Date(this.vsData[0].time).toLocaleDateString();
        this.showChart = true;
        if(this.vsData[0][vs] == undefined){
            // there is no data for this vital sign. loop over the source and update the vs instead
            let vss = ['hr', 'rr', 'spo2', 'temp', 'bp'];
            for(var i in vss){
                if(this.vsData[0][vss[i]] != undefined){
                    vs = vss[i];
                    this.showChart = false;
                    break;
                }
            }

            // no vs data given
            if(this.showChart){
                return;
            }
        }

        // update the range of the value
        // valueMin: min(min(values), normal_range[vs]) .. 
        this.valueMin = this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_l"];
        this.valueMax = this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_h"];


        
        // if there are any data
        for(var i in this.vsData){
            // update valueMin
            if(this.vsData[i][vs][this.stat] < this.valueMin){
                this.valueMin = this.vsData[i][vs][this.stat];
            }

            // update valueMax
            if(this.vsData[i][vs][this.stat] > this.valueMax){
                this.valueMax = this.vsData[i][vs][this.stat];
            }

            var tuple = {time: this.vsData[i].time};
            tuple['value'] = this.vsData[i][vs][this.stat];
            this.dataDisplay.push(tuple)
        }
        
        // update this.dataRange (min-max)
        if(this.showMinMax){
            this.dataRange = [];
            for(var i in this.vsData){
                var tuple = {time: this.vsData[i].time};
                tuple['value'] = [
                    this.vsData[i][vs]['min'],
                    this.vsData[i][vs]['max'],
                ];
                this.dataRange.push(tuple)
            }
        }

        // update this.dataStdev
        if(this.showStdev){
            this.dataStdev = [];
            for(var i in this.vsData){
                var tuple = {time: this.vsData[i].time};
                tuple['value'] = [
                    parseFloat((this.vsData[i][vs][this.stat] - this.vsData[i][vs]['std'] / 2).toFixed(2)),
                    parseFloat((this.vsData[i][vs][this.stat] + this.vsData[i][vs]['std'] / 2).toFixed(2))
                ];
                this.dataStdev.push(tuple)
            }
        }


        if(this.showAbnormal){
            annotations = [
                        // min
                        {
                            type: 'text',
                            position: ['min', this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_l"] ],
                            content: `Low = ${this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_l"]}`,
                            offsetY: -4,
                            style: {
                                textBaseline: 'bottom',
                            },
                        },
                        {
                            type: 'line',
                            start: ['min', this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_l"] ],
                            end: ['max', this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_l"] ],
                            style: {
                                stroke: '#F4664A',
                                lineDash: [2, 2],
                            },
                        },

                        // max
                        {
                            type: 'text',
                            position: ['min', this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_h"] ],
                            content: `High = ${this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_h"]}`,
                            offsetY: -4,
                            style: {
                                textBaseline: 'bottom',
                            },
                        },
                        {
                            type: 'line',
                            start: ['min', this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_h"] ],
                            end: ['max', this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_h"] ],
                            style: {
                                stroke: '#F4664A',
                                lineDash: [2, 2],
                            },
                        },
                    ];
        }
        
        
        if(!this.showChart){
            annotations.push({
                type:"region",
                start: ['min', 'min'],
                end: ['max', 'max'],
                top:true,
                style:{
                    fill: "#666",
                    fillOpacity: 0.5,
                }
            });
            annotations.push({
              type:"text",
              position: ["40%", "45%"],
              top:true,
              content:`No Data`,
              style:{
                fontSize: "40",
                fill: "#fff",
              }
            });
        }
        

        var viewData = {
                    data: this.dataDisplay,
                    axes: {},
                    meta: {
                        time: {
                            type: 'time',
                            mask: 'HH:mm',
                            nice: true,
                            range: [0, 1],
                        },
                        value: {
                            nice: true,
                            sync: true,
                            alias: 'Value',
                            min: this.valueMin - 2,
                            max: this.valueMax + 2,
                        },
                        
                    },
                    annotations: annotations,
                    // view2: prepare a line plot, mapping position to `time*temperature`
                    geometries: [
                        {
                            type: 'line',
                            xField: 'time',
                            yField: 'value',
                            mapping: {},
                        },
                        {
                            type: 'point',
                            xField: 'time',
                            yField: 'value',
                            colorField: 'value', // 
                            mapping: {
                                color: ({ value }) => {
                                    var val = parseFloat(value.toFixed(1));
                                    if((val < this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_l"] 
                                        || val > this.$store.getters.patients[this.$route.params.id].normal_range[vs + "_h"] )
                                        && this.showAbnormal
                                    ){
                                        return '#ed1558';
                                    }
                                    return '#165aed';
                                },
                                shape: 'circle',
                                style: {
                                    fillOpacity: 1,
                                },
                            },
                        },
                    ],
                };
     
        var viewRange = {
                    data: this.dataRange,
                    axes: false,
                    meta: {
                        time: {
                            type: 'time',
                            mask: 'HH:mm',
                            nice: true,
                            range: [0, 1],
                        },
                        value: {
                            nice: true,
                            sync: true,
                            alias: 'Min-Max Range',
                        },
                    },
                    // view1: prepare a area plot, mapping position to `time*temperature`
                    geometries: [
                        {
                            type: 'area',
                            xField: 'time',
                            yField: 'value',
                            mapping: {},
                        },
                    ],
                };
        
        
        var viewStdev = {
                    data: this.dataStdev,
                    axes: false,
                    meta: {
                        time: {
                            type: 'time',
                            mask: 'HH:mm',
                            nice: true,
                            range: [0, 1],
                        },
                        value: {
                            nice: true,
                            sync: true,
                            alias: 'Stdev Range',
                        },
                    },
                    // view3: prepare a interval plot, mapping position to `time*temperature`
                    geometries: [
                        {
                            type: 'area',
                            xField: 'time',
                            yField: 'value',
                            mapping: {
                                color: "#ff8c00"
                            },
                            
                        },
                    ],
                };
        views.push(viewData);
        if(this.showMinMax){
            views.push(viewRange);
        }
        if(this.showStdev){
            views.push(viewStdev);
        }
        console.log(views.length);

        // update the chart
        this.chart.update({
            appendPadding: 2,
            syncViewPadding: true,
            tooltip: { shared: true, showMarkers: false, showCrosshairs: true, offsetY: -50 },
            views:views
        });
        console.log(views);
    },

    mounted(){
        this.chart = new MultiView('container', {
            appendPadding: 2,
            syncViewPadding: true,
            tooltip: { shared: true, showMarkers: false, showCrosshairs: true, offsetY: -50 },
            
        });
        this.chart.render();
    },
    

    methods:{
        forceUpdatePage(){
            this.$forceUpdate();
        },
    },

})
</script>

<style>

</style>
