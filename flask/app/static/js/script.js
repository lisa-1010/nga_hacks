var colors = ['#ffffff', '#ffffe0','#ffd4ad','#ffa77a','#ff7246','#ff0000'];
var numPrefectures = 34;

var populationRanges = ['<150000', '150000-200000', '200000-275000', '275000-295000', '295000-350000', '>350000']
var population = {'Beyla': 26,
'Boffa': 13,
'Boke': 31,
'Conakry': 34,
'Coyah': 15,
'Dabola': 9,
'Dalaba': 5,
'Dinguiraye': 11,
'Dubreka': 27,
'Faranah': 18,
'Forecariah': 14,
'Fria': 1,
'Gaoual': 10,
'Gueckedou': 22,
'Kankan': 32,
'Kerouane': 12,
'Kindia': 30,
'Kissidougou': 19,
'Koubia': 2,
'Koundara': 4,
'Kouroussa': 16,
'Labe': 24,
'Lelouma': 6,
'Lola': 7,
'Macenta': 23,
'Mali': 21,
'Mamou': 25,
'Mandiana': 28,
'Nzerekore': 29,
'Pita': 17,
'Siguiri': 33,
'Telimele': 20,
'Tougue': 3,
'Yomou': 8};

$(document).ready(function() {
  $('svg').find('path').each(function(index, province) {
    $(province).click(function() {
      var index = parseInt($(province).attr('index'));
      console.log(index)
      $(province).attr('fill', colors[(index + 1) % colors.length]);
      $(province).attr('index', (index + 1) % colors.length);
    });
  });

  $('#gradient').html(getGradientHTML());

  $('.population').click(function() {
    createPopulationMap();
  });
});

function getGradientHTML() {
  var html = '';
  for (var i = 0; i < colors.length; i++) {
    html += '<td bgcolor="' + colors[i] + '">&nbsp;' + populationRanges[i] + '&nbsp;</td>';
  }
  return html;
}

function createPopulationMap() {
  $('svg').find('path').each(function(index, province) {
    var name = $(province).attr('data-name');
    var count = population[name];
    $(province).attr('fill', getGradientColor(count));
  });
};

function getGradientColor(count) {
  var intervalSize = numPrefectures / colors.length;
  return colors[Math.floor((count - 1) / intervalSize)];
}
