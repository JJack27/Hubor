import { MultiView } from '@antv/g2plot';

fetch('https://gw.alipayobjects.com/os/antfincdn/qE48lpzwRc/range-area-data.json')
  .then((data) => data.json())
  .then((data) => {
    const { area: data1, line: data2 } = data;
    const rangeAreaPlot = new MultiView('container', {
      appendPadding: 8,
      syncViewPadding: true,
      tooltip: { shared: true, showMarkers: true, showCrosshairs: true, offsetY: -50 },
      plots:[
        {
          type:'area',
          options: {
            interactions: [
              { type: 'brush-x' },
            ],
            showMarkers:true,
            data: data1,
            xField: 'time',
            yField: 'temperature',
            yAxis:{
              min:0,
              max:45,
            },
            line:{
              size: 0.0,
            },
            meta:{
              time:{
                type: 'time',
                mask: 'MM-DD',
                nice: true,
                tickInterval: 24 * 3600 * 1000 * 2,
              }
            }
          }
        },

        {
          type: 'line',
          options: {
            data: data2,
            xField: 'time',
            yField: 'temperature',
            padding: 'auto',
            showMarkers: true,
            yAxis:{
              min:0,
              max:45,
            },
            top:true,
            
            meta:{
              time:{
                type: 'time',
                mask: 'MM-DD',
                nice: true,
                tickInterval: 24 * 3600 * 1000 * 2,
              }
            },
            smooth:true,
            annotations:[
              {
                type:"regionFilter",
                start:['min', "min"],
                end:["max", "median"],
                color: '#F4664A',
              }
            ],
            marker:{
              style:{
                stroke: 'red',
              }
            },
            interactions: [
              { type: 'brush-x' },
              { type: 'element-single-highlight'},
              ],
          },
        },
      ]
    });

    // Step 3: 渲染图表
    rangeAreaPlot.render();
  });
