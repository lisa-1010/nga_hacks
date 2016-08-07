$(document).ready(function() {
  var INACTIVE = 0
  var ACTIVE = 1

  var state = {}

  function colorProvince($province, id) {
    if (state[id]['isActive']) {
      $province.attr('fill', 'red');
    } else {
      $province.attr('fill', 'white');
    }
  }

  function createRow($province) {
    var $row = $('<div></div>').attr('id', 't-' + $province.attr('id'));
    
    var $col1 = $('<div></div>').html($province.attr('data-name')).attr('class', 'A');
    var $col2 = $('<div></div>').html("B").attr('class', 'B');
    var $col3 = $('<div></div>').html(state[$province.attr('id')]['numTreatmentCenters']).attr('class', 'C');


    // var $col1 = $('<div></div>').html($province.attr('data-name')).attr({class: 'col'});
    // var $col2 = $('<div></div>').attr({class: 'chart'});
    // var $col3 = $('<div></div>').html(state[$province.attr('id')]['numTreatmentCenters']).attr({class: 'col'});

    $row.append($col1);
    $row.append($col2);
    $row.append($col3);

    return $row
  }

  var $treatmentCenters = $('#treatment-centers');
  $('svg').find('path').each(function(index, province) {
    var $province = $(province);
    var id = $province.attr('id');

    state[id] = {}
    state[id]['isActive'] = false;
    state[id]['numTreatmentCenters'] = 0;

    // Attaches event listeners to the path
    $province.on('click', function() {
      state[id]['isActive'] = !state[id]['isActive'];
      colorProvince($province, id);

      var $elem = $('#t-' + id);
      console.log($elem);
      var scrollPosition = $elem.position().top;
      $('#treatment-centers').animate({scrollTop: scrollPosition});
    });
    $province.hover(function() {
      $province.attr('fill', 'blue');
    }, function() {
      colorProvince($province, id);
    })

    // Creates the Treatment Center element in table
    $treatmentCenters.append(createRow($province));
    $treatmentCenters.append($('<div></div>').attr('class', 'ui divider'));
  });


});
