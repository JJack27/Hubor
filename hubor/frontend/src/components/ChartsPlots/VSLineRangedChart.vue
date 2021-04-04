<template>
    <div id="container">

    </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { MultiView } from '@antv/g2plot';

export default defineComponent({
    name:"VSLineRangedChart",
    inject:[
        'id',
    ],
    data(){
        return{
            aType: "min",
            toTime: null,
            fromTime: null,
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
            console.log(oneHr);
            console.log(anHrBeforeNow.toJSON())
            return anHrBeforeNow.toJSON();
        }

    },

    mounted(){
        this.$get(`/api/vitalsign/${this.id}/?from=${this.oneHrBeforeNow}&to=${this.now}&type=${this.aType}`)
            .then(response => {
                console.log(response);
            });
    },

    setup() {
        //console.log(`api/vitalsign/${this.id}/?from=${fromTime._rawValue}&to=${toTime._rawValue}&time=${type._rawValue}`);
        
        /*
        const chart = this.$get('api/vitalsign/?from=%s&to=%s&time=&type'%(fromTime, toTime, type))
            .then((response) => {
                const { area: data1, line: data2 } = data;
                const rangeAreaPlot = new MultiView('container', {
                    appendPadding: 8,
                    syncViewPadding: true,
                    tooltip: { shared: true, showMarkers: false, showCrosshairs: true, offsetY: -50 },
                    views: [
                        {
                            data: data1,
                            axes: {},
                            meta: {
                                time: {
                                    type: 'time',
                                    mask: 'MM-DD',
                                    nice: true,
                                    tickInterval: 24 * 3600 * 1000 * 2,
                                    range: [0, 1],
                                },
                                temperature: {
                                    nice: true,
                                    sync: true,
                                    alias: '温度范围',
                                },
                            },
                            // view1: prepare a area plot, mapping position to `time*temperature`
                            geometries: [
                                {
                                    type: 'area',
                                    xField: 'time',
                                    yField: 'temperature',
                                    mapping: {},
                                },
                            ],
                        },
                        {
                            data: data2,
                            axes: false,
                            meta: {
                                time: {
                                    type: 'time',
                                    mask: 'MM-DD',
                                    nice: true,
                                    tickInterval: 24 * 3600 * 1000 * 2,
                                    range: [0, 1],
                                },
                                temperature: {
                                    sync: 'temperature',
                                    alias: '温度',
                                },
                            },
                            // view2: prepare a line plot and point plot, mapping position to `time*temperature` (share data)
                            geometries: [
                                {
                                    type: 'line',
                                    xField: 'time',
                                    yField: 'temperature',
                                    mapping: {},
                                },
                                {
                                    type: 'point',
                                    xField: 'time',
                                    yField: 'temperature',
                                    mapping: {
                                        shape: 'circle',
                                        style: {
                                            fillOpacity: 1,
                                        },
                                    },
                                },
                            ],
                        },
                    ],
                });

            // Step 3: 渲染图表
            rangeAreaPlot.render();
        });
        */
        return {
        };
    },


})
</script>

<style>

</style>
