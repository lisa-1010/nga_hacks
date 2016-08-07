function clickEvent() {
    console.log('hi');
}

$(document).ready(function() {
  // TODO - broken
  // $('svg').find('path').each(function(index, province) { 
  //  var $province = $(province)
  //  $province.on('click', function() {
  //    console.log('hi');
  //  });
  // });
  var paths = document.querySelectorAll('svg path');
  for (var i = 0; i < paths.length; i++) {
    (function() {
      var path = paths[i];
      path.addEventListener('click', function(event) {
        event.preventDefault()
        console.log('here')
      })
    })();
  }

  // .forEach(function(element) {
  //  element.addEventListener('click', function() {
  //    console.log('here');
  //  });
  // });
});
