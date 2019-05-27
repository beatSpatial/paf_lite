$(function(){
      // create slider
  function createSlider(peers, peer_lookup){
    // create handles
    $('#slider').slider({
        // set min and maximum values
        // day hours in this example
        min: 0,
        max: 10,
        // step
        // quarter of an hour in this example
        step: 0.25,
        // range
        range: false,
        // show tooltips
        tooltips: true,
        // current data
        handles: peers,
        // display type names
        showTypeNames: true,
        typeNames: peer_lookup,
        // main css class (of unset data)
        //mainClass: "27k",// 'the myself student',
        // slide callback
        slide: function(e, ui) {
          console.log(e, ui);
        },
        // handle clicked callback
        handleActivated: function(event, handle) {
          // get select element
          var select = $(this).parent().find('.slider-controller select');
          // set selected option
          select.val(handle.type);
        }
      });
  };

  function renderTeamMembers(pword){

    $.ajax({
      url: $("#js-team-options").attr('js-get-team-options-url'),
      async: true,
      type: "GET",
      data: {
          'pass': pword,
          },
      dataType: 'json',
      success: function(result){
        createSlider(result[0], result[1])
      },
      error : function(xhr, errmsg, err) {

        // add error to the dom
        $('#js-results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! There has been an error.</div>");

        // Provide error detail to the console
        console.log(xhr.status + ": " + xhr.responseText);
      }
    })
  };


    $('#team').click(function(){
        var pword = $('#pass').val()
        renderTeamMembers(pword)
    });

    // function to create slider ticks
  var setSliderTicks = function() {
    // slider element
    var $slider = $('.slider');
    var max = $slider.slider("option", "max");
    var min = $slider.slider("option", "min");
    var step = $slider.slider("option", "step");
    var spacing = 100 / (max - min);
    // tick element
    var ticks = $slider.find('div.ticks');

    // remove all ticks if they exist
    $slider.find('.ui-slider-tick-mark-main').remove();
    $slider.find('.ui-slider-tick-mark-text').remove();
    $slider.find('.ui-slider-tick-mark-side').remove();

    // generate ticks
    for (var i = min; i <= max; i = i + step) {

      // main ticks (whole number)
      if (i % 1 === 0) {
        $('<span class="ui-slider-tick-mark-main"></span>').css('left', (spacing * i) + '%').appendTo(ticks);
        $('<span class="ui-slider-tick-mark-text">' + i + '</span>').css('left', (spacing * i) + '%').appendTo(ticks);
      }
      // side ticks
      else {
        $('<span class="ui-slider-tick-mark-side"></span>').css('left', (spacing * i) + '%').appendTo(ticks);
      }
    }
  };




  // when clicking on handler
  $(document).on('click', '.slider a', function() {
    var select = $('.slider-controller select');
    // enable if disabled
    //select.attr('disabled', false);
    alert($(this).attr('data-type'));
    select.val($(this).attr('data-type'));
    /*if ($(this).parent().find('a.ui-state-active').length)
      $(this).toggleClass('ui-state-active');*/
  });

  $('#assess').click(function() {

    $.ajax({
      url: $("#slider").attr('js-get-team-alloc-url'),
      async: true,
      type: "GET",
      data: {
          'pass': $('#pass').val(),
          'alloc': JSON.stringify($('#slider').slider('values')),
          'phase': $('#phase').val()
          },
      dataType: 'json',
      success: function(result){
        //createSlider(result[0], result[1])
      },
      error : function(xhr, errmsg, err) {

        // add error to the dom
        $('#js-results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! There has been an error.</div>");

        // Provide error detail to the console
        console.log(xhr.status + ": " + xhr.responseText);
      }
    })
  });

  $("#id_country").change(function () {
      var url = $("#personForm").attr("data-cities-url");  // get the url of the `load_cities` view
      var countryId = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': countryId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#id_city").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });

    });

 
});