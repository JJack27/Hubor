<template>
    <div>
        <a-row type="flex" justify="center" align="middle">
            <a-col :span="1">
                <img
                    :src="require(`@/assets/icons/${this.vs}_icon.png`)"
                    height="20"
                    width="20"
                    style="margin-top:-7pt;"
                >
            </a-col>
            <a-col :span="5">
                <h1 style="text-transform: capitalize;"> {{this.vs}} - {{this.stat}} </h1>
            </a-col>
        </a-row>
        
        
        <div id="container">
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, inject } from 'vue';
import { Area } from '@antv/g2plot';

export default defineComponent({
    name:"VSAreaChart",
    props:[
        'vsData',
        'vs',    // hr, rr, spo2...
        'stat',     // mean, max, min, median, stdev
        'timeSpan', // min, hr, day,   
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
        this.dataDisplay = []
        this.valueMin = this.vsData[0][this.vs][this.stat];
        this.valueMax = this.vsData[0][this.vs][this.stat];
        for(var i in this.vsData){
            if(this.vsData[i][this.vs][this.stat] < this.valueMin){
                this.valueMin = this.vsData[i][this.vs][this.stat];
            }

            if(this.vsData[i][this.vs][this.stat] > this.valueMax){
                this.valueMax = this.vsData[i][this.vs][this.stat];
            }

            var tuple = {time: this.vsData[i].time};
            tuple['value'] = this.vsData[i][this.vs][this.stat];
            this.dataDisplay.push(tuple)
        }
        console.log(this.dataDisplay);
        var range = {
            yAxis:{
                min: this.valueMin - 2,
                max: this.valueMax + 2,
            },
        }
        
        this.area.changeData(this.dataDisplay);
        this.area.update(range);
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
