var localites = ['dalaba', 'dabola', 'siguiri', 'kankan', 'nzerekore', 'yomou', 'dubreka', 'dinguiraye', 'lola', 'gueckedou', 'boke', 'kerouane', 'kindia', 'telimele', 'forecariah', 'coyah', 'kouroussa', 'beyla', 'boffa', 'kissidougou', 'mamou', 'faranah', 'macenta', 'pita', 'conakry'];

$(function () {
  function createChart($chart, enabled) {
    $chart.highcharts({
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
        tickLength: 0,
        labels: {
          style: {
            fontSize:'9px'
          },
          enabled: enabled
        }
      },
      yAxis: {
        title: '',
        lineWidth: 1,
        gridLineWidth: 0,
        minorGridLineWidth: 0,
        labels: {
          style: {
            fontSize:'9px'
          },
          enabled: enabled
        }
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
  }

  createChart($('#outbreak-effect'), true);
  
  var charts = []
  $('#treatment-centers').find('div').each(function(i, row) {
    $row = $(row);
    $col = $row.find('.B');
    charts.push($col);
  });

  charts.forEach(function($chart, i) {
    createChart($chart, false)
  });

  (function() {
    $.get('/api/charts', {"macenta": 2, "coyah": 1, "kerouane": 1}, function(response, status) {
      /// TODO - status code
      for (localite in response) {
        var data = parseStringArray(response[localite]);
        console.log(data);
      }
    }, 'json');
  })();

  function parseStringArray(string) {
    return string.map(parseFloat);
  }
});
