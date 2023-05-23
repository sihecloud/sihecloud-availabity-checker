function getVirtualData(year) {
    const date = +echarts.time.parse(year + '-01-01');
    const end = +echarts.time.parse(+year + 1 + '-01-01');
    const dayTime = 3600 * 24 * 1000;
    const data = [];
    for (let time = date; time < end; time += dayTime) {
        data.push([
            echarts.time.format(time, '{yyyy}-{MM}-{dd}', false),
            Math.random() * 1.0,
        ]);
    }
    return data;
}

function drawHeatMapByDate(element, data) {
    var myChart = echarts.init(element);

    option = {
        title: {
            top: 30,
            left: 'center',
            text: '可用性热力图（2023年）'
        },
        visualMap: {
            min: 0,
            max: 100,
            type: 'piecewise',
            orient: 'horizontal',
            left: 'center',
            top: 65,
            inRange: {
                color: ['#ececef', '#f9ffd2', '#c4eb9a', '#73e383', '#449c4e']
            }

        },
        calendar: {
            top: 120,
            left: 30,
            right: 30,
            cellSize: ['30', '22'],
            range: '2023',
            itemStyle: {
                borderWidth: 0.5
            },
            yearLabel: { show: true }
        },
        tooltip: {
            formatter: function (params) {
                var value = params.data[1];
                var percentage = (value).toFixed(2) + '%';
                return params.data[0] + '<br>可用性: ' + percentage;
            },
        },
        series: {
            type: 'heatmap',
            coordinateSystem: 'calendar',
            data: data
        }
    };
    myChart.setOption(option);
}


function drawHeatMapRecent(element, days, hours, data) {
    var myChart = echarts.init(element);

    option = {
        title: {
            top: 0,
            left: 'center',
            text: '可用性热力图(近七天, 按小时）'
        },

        tooltip: {
            position: 'top',
            formatter: function (params) {
                var value = params.data[2];
                var percentage = (value).toFixed(2) + '%';
                return (
                    days[params.data[1]] +
                    ' ' +
                    hours[params.data[0]] +
                    '<br>可用性: ' +
                    percentage
                );
            }
        },
        grid: {
            top: '80px'
        },
        xAxis: {
            type: 'category',
            data: hours,
            splitArea: {
                show: true
            }
        },
        yAxis: {
            type: 'category',
            data: days,
            splitArea: {
                show: true
            }
        },
        visualMap: {
            min: 0,
            max: 100,
            calculable: true,
            type: 'piecewise',
            orient: 'horizontal',
            left: 'center',
            top: 30,
            inRange: {
                color: ['#ececef', '#f9ffd2', '#c4eb9a', '#73e383', '#449c4e']
            }
        },
        series: [
            {
                name: '',
                type: 'heatmap',
                data: data,
                label: {
                    show: true,
                    formatter: (params) => {
                        return (params.data[2]).toFixed(0);
                    }
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    myChart.setOption(option);

}