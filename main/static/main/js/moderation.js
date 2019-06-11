$(function(){

  $('input[type="checkbox"]').change(function(e){
        var ratingId = $(this).attr('id');
        phase = $('#js-phase').val()

        var url = $("#alloc").attr("toggle-single-alloc-url")
        $.ajax({
            url: url,
            data: {
                'pk': ratingId,
                'phase': phase
            },
            success: function(data) {
                e.preventDefault()
                $("#dynamic_table").html(data)
                return false
            }
        })
    });
});