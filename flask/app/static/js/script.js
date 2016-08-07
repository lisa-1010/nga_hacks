$(document).ready(function() {
  $('svg').find('path').each(function(index, province) { 
   var $province = $(province)
   $province.on('click', function() {
     console.log('hi');
   });
  });
});
