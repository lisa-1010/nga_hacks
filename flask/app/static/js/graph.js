$(function () {
  $('#outbreak-effect-chart').highcharts({
    chart: {
      backgroundColor: '#fcfcfc',
      type: 'line'
    },
    title: {
      text: ''
    },
    plotOptions: {
      series: {
        marker: {
          enabled: false
        }
      }
    },
    minorGridLineWidth: 0,
    xAxis: {
      lineWidth: 1,
      tickLength: 0
    },
    yAxis: {
      title: '',
      lineWidth: 1,
      gridLineWidth: 0,
      minorGridLineWidth: 0,
    },
    series: [{
      name: 'ETC-0',
      data: [1, 0, 4, 8, 5, 6, 8, 7, 9, 12, 14, 15, 16, 15, 16, 17]
    }, {
      name: 'ETC-N',
      data: [2, 1, 3, 4, 7, 6, 5, 6, 9, 10, 12, 13, 15, 14, 17, 18]
    }],
    credits: {
        enabled: false
    },
    legend: {
                 enabled: false
             }

  });
});
