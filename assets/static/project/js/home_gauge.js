function crearGauge(contenedorId) {
    return Highcharts.chart(contenedorId, {
        chart: {
            type: 'gauge',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false,
            height: '40%',
        },
        credits: {
            enabled: false
        },
        title: {
            text: null
        },

        pane: {
            startAngle: -90,
            endAngle: 90,
            background: null,
            center: ['50%', '70%'],
            size: '140%'
        },
        // the value axis
        yAxis: {
            min: 0,
            max: 120,
            tickPixelInterval: 72,
            tickPosition: 'inside',
            tickColor: Highcharts.defaultOptions.chart.backgroundColor || '#FFFFFF',
            tickLength: 20,
            tickWidth: 2,
            minorTickInterval: null,
            labels: {
                distance: -35,
                style: {
                    fontSize: '14px'
                }
            },
            lineWidth: 0,
            plotBands: [
            {
                from: -50,
                to: 10,
                color: '#0000FF', // blue
                thickness: 20,
                borderRadius: '50%'
            },
            {
                from: -5,
                to: 30,
                color: 'cyan', // cyan
                thickness: 20,
            },
            {
                from: 30,
                to: 50,
                color: 'orange', // yellow
                thickness: 20,
            },
            {
                from: 80,
                to: 120,
                color: '#FF0000', // red
                thickness: 20,
                borderRadius: '50%'
            },
            {
                from: 50,
                to: 85,
                color: '#DF5353', // red
                thickness: 20,
            },
        ]
        },
        series: [{
            name: '',
            data: [0],
            dataLabels: {
                borderWidth: 0,
                style: {
                    fontSize: '16px'
                }
            },
            dial: {
                radius: '100%',
                backgroundColor: 'blue',
                baseWidth: 12,
                baseLength: '0%',
                rearLength: '0%'
            },
            pivot: {
                backgroundColor: 'gray',
                radius: 6
            }
        }]
    });
}
