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
    mounted(){
        //console.log(`api/vitalsign/${this.id}/?from=${fromTime._rawValue}&to=${toTime._rawValue}&time=${type._rawValue}`);
        fetch('https://gw.alipayobjects.com/os/bmw-prod/1d565782-dde4-4bb6-8946-ea6a38ccf184.json')
        .then((res) => res.json())
        .then((data) => {
            this.area = new Area('container', {
            data,
            xField: 'Date',
            yField: 'scales',
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
        });
    },
    

    methods:{
        test(){
            console.log(this.vsData);
        }
    }

})
</script>

<style>

</style>
