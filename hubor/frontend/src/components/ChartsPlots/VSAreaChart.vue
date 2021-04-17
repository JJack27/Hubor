<template>
    <div id="container">

    </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { Area } from '@antv/g2plot';

export default defineComponent({
    name:"VSAreaChart",
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
        this.$get(`/api/latest1hourvs/${this.id}/`)
            .then(response => {
                console.log(response);
            });
    },

    setup() {
        //console.log(`api/vitalsign/${this.id}/?from=${fromTime._rawValue}&to=${toTime._rawValue}&time=${type._rawValue}`);
        fetch('https://gw.alipayobjects.com/os/bmw-prod/1d565782-dde4-4bb6-8946-ea6a38ccf184.json')
        .then((res) => res.json())
        .then((data) => {
            const area = new Area('container', {
            data,
            xField: 'Date',
            yField: 'scales',
            annotations: [
                {
                    type: 'text',
                    position: ['min', 'median'],
                    content: '中位数',
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
            area.render();
        });
        return {
        };
    },


})
</script>

<style>

</style>
