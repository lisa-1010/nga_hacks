var colors = ['#ffffff', '#ffffe0','#ffd4ad','#ffa77a','#ff7246','#ff0000'];

$(document).ready(function() {
  $('svg').find('path').each(function(index, province) {
    $(province).on('click', function() {
      var index = parseInt($(province).attr('index'));
      console.log(index)
      $(province).attr('fill', colors[(index + 1) % colors.length]);
      $(province).attr('index', (index + 1) % colors.length);
    });
  });

  $('#gradient').html(getGradientHTML());
});

function getGradientHTML() {
  var html = '';
  for (var i = 0; i < colors.length; i++) {
    html += '<div style="width: 16.6667%; height: 100%; background: ' + colors[i] + ';"></div>';
  }
  return html;
}