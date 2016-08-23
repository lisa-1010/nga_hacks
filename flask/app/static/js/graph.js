var initialData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

var keys = ['beyla',
'boffa',
'boke',
'conakry',
'coyah',
'dabola',
'dalaba',
'dinguiraye',
'dubreka',
'faranah',
'forecariah',
'fria',
'gaoual',
'gueckedou',
'kankan',
'kerouane',
'kindia',
'kissidougou',
'koubia',
'koundara',
'kouroussa',
'labe',
'lelouma',
'lola',
'macenta',
'mali',
'mamou',
'mandiana',
'nzerekore',
'pita',
'siguiri',
'telimele',
'tougue',
'yomou'];

$(function () {
  function createChart($chart, enabled, etc0, etc1) {
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
        data: etc0
      }, {
        name: 'ETC-N',
        data: etc1
      }],
      credits: {
          enabled: false
      },
      legend: {
        enabled: false
      }
    });
  }

  createChart($('#outbreak-effect'), true, initialData, initialData);
  
  var charts = []
  $('#treatment-centers').find('div').each(function(i, row) {
    $row = $(row);
    $col = $row.find('.B');
    charts.push($col);
  });

  charts.forEach(function($chart, i) {
    createChart($chart, false, initialData, initialData);
  });

  (function() {
    $.ajax({
      contentType: 'application/json',
      data: JSON.stringify({'macenta': 2, 'coyah': 1, 'kerouane': 1}),
      dataType: 'json',
      type: 'POST',
      url: '/api/charts',
      success: function(response, status) {
        for (var name in response) {
          var index = getIndex(name);
          console.log(name + " " + index);

          var etc0 = stringToFloatArray(response[name][0]);
          var etc1 = stringToFloatArray(response[name][1]);
          console.log(etc0);
          console.log(etc1);

          var $chart = $('[data-highcharts-chart=' + index + ']');
          createChart($chart, false, etc0, etc1);
        }
      },
      error: function() {
          app.log("Device control failed");
      }
    });
  })();

  function getIndex(name) {
    for (var i = 0; i < keys.length; i++) {
      if (keys[i] === name) return i + 1;
    }
    return -1;
  }

  function stringToFloatArray(stringArray) {
    return stringArray.map(parseFloat);
  }
});
