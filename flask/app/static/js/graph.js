$(function () {
  $('#outbreak-effect-chart').highcharts({
    chart: {
      type: 'line'
    },
    title: {
      text: ''
    },
    xAxis: {
      categories: ['Apples', 'Bananas', 'Oranges']
    },
    yAxis: {
      title: {
        text: 'Fruit eaten'
      }
    },
    series: [{
      name: 'Jane',
      data: [1, 0, 4]
    }, {
      name: 'John',
      data: [2, 1, 3, 4, 7, 6, 5, 6, 9, 10, 12, 13, 15, 14, 17, 18, 20]
    }]
  });
});
