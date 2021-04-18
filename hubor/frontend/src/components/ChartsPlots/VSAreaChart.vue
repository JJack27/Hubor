<template>
    <div>
        <div id="container">

        </div>
        <a-button @click="test">test</a-button>
    </div>
</template>

<script>
import { defineComponent, ref, inject } from 'vue';
import { Area } from '@antv/g2plot';

export default defineComponent({
    name:"VSAreaChart",
    props:[
        'vsData',
    ],
    data(){
        return{
            aType: "min",
            toTime: null,
            fromTime: null,
            area: null,
            dataDisplay: [],
            valueMin: 10000,
            valueMax: -10000,
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
    beforeUnmount(){
        this.area.destroy();
    },

    updated(){
        this.valueMin = this.vsData[0]['hr']['mean'];
        this.valueMax = this.vsData[0]['hr']['mean'];
        for(var i in this.vsData){
            if(this.vsData[i]['hr']['mean'] < this.valueMin){
                this.valueMin = this.vsData[i]['hr']['mean'];
            }

            if(this.vsData[i]['hr']['mean'] > this.valueMax){
                this.valueMax = this.vsData[i]['hr']['mean'];
            }

            this.dataDisplay.push(
                {time: this.vsData[i].time, value: this.vsData[i].hr.mean}
            )
        }
        console.log(this.dataDisplay);
        this.area.changeData(this.dataDisplay);
    },

    mounted(){
        this.area = new Area('container', {
            data: this.vsData,
            xField: 'time',
            yField: 'value',
            smooth: true,
            yAxis:{
                min: this.valueMin - 5,
                max: this.valueMax + 5,
            },
            annotations: [
                {
                    type: 'text',
                    position: ['min', 'median'],
                    content: 'Median',
                    offsetY: -4,
                    style: {
                        textBaseline: 'bottom',
                },
                },
                {
                    type: 'line',
                    start: ['min', 'median'],
                    end: ['max', 'median'],
                    style: {
                        stroke: 'red',
                        lineDash: [2, 2],
                    },
                },
            ],
        });
        this.area.render();
        
    },
    

    methods:{
        test(){
            this.area.update();
            console.log(this.vsData);
        }
    }

})
</script>

<style>

</style>
