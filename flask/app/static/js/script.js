var colors = ['#ffffe0','#ffd4ad','#ffa77a','#ff7246','#ff0000'];

$(document).ready(function() {
  $('svg').find('path').each(function(index, province) {
    $(province).on('click', function() {
      var index = parseInt($(province).attr('index'));
      console.log(index)
      $(province).attr('fill', colors[(index + 1) % colors.length]);
      $(province).attr('index', (index + 1) % colors.length);
    });
  });
});
