$(document).ready(function() {
  $('svg').find('path').each(function(index, province) {
    $(province).on('click', function() {
      if ($(province).attr('fill') === 'white') {
        $(province).attr('fill', 'red');
      } else {
        $(province).attr('fill', 'white');
      }
    });
  });
});
