$(function(){
    var bgClassList = [
    'bg-primary',
     'bg-success',
      'bg-info',
       'bg-warning',
        'bg-danger',
         'bg-secondary',
          'bg-dark',
           'bg-light']


      // create slider
  function createSlider(peers, peer_lookup){
    // create handles
    $('#slider').slider({
        // set min and maximum values

        min: 0,
        max: 10,
        // step
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
          console.log(e, ui)
        },
        // handle clicked callback
        handleActivated: function(event, handle) {
          // get select element
          var select = $(this).parent().find('.slider-controller select');
          // set selected option
          select.val(handle.type);
        }
      });

      $("#slider .ui-slider-handle").unbind('keydown');
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
        // Prevents first handle moving
        $("a[data-value='0']").on('mousedown', function(e){
            e.stopImmediatePropagation();
            return false;
        })
        console.log($( ".ui-slider-handle"))
        var ranges = $( ".ui-slider-range")
        var handles = $( ".ui-slider-handle" )
        $.each(handles, function(i, handle){
            console.log(i, handle)
            let idx = i;
            $(handle).data('temperature', 'index'+idx)
            $(handle).addClass('index'+idx)
        })

        $.each(ranges, function(i, range){
            console.log(i, range)
            let idx = i;
            $(range).data('temperature', 'index'+idx)
            $(range).addClass('index'+idx)
        })
        // show the button
        $('#assess').show()
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
    select.val($(this).attr('data-type'));
    /*if ($(this).parent().find('a.ui-state-active').length)
      $(this).toggleClass('ui-state-active');*/
  });

  $('#assess').hide()
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
        alert('Team member scores logged')
        window.location.reload()
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

  $('input[type="checkbox"]').change(function(){
    // Processing only those that match the name attribute of the currently clicked button...
    //$('input[name="' + $(this).attr('name') + '"]').not($(this)).trigger('deselect');

    // TODO sillyscores to a button
    if($(this).attr('name') == 'sillyscores'){

        // Get student id with which to locate their allocations
        var studentId = $(this).attr('id');
        var phase = $("select#js-phase option:checked").val();
        // get url from dom
        var url = $("#alloc").attr("toggle-total-alloc-url")
        $.ajax({
            url: url,
            data: {
                'pk': studentId,
                'phase': phase
            },
            success: function(data) {
                window.location.reload()
            }
        })
    } else {
        var ratingId = $(this).attr('id');
        var url = $("#alloc").attr("toggle-single-alloc-url")
        $.ajax({
            url: url,
            data: {
                'pk': ratingId,
            },
            success: function(data) {
                window.location.reload()
            }

        })
    }
    });




});