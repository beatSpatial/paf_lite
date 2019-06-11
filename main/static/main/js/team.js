$(function(){

    $('#get_team').submit(function(e) {
        e.preventDefault();
        var chosen_phase = $('#js-phase').val()

        //$('#phase').val(chosen_phase)
        var class_no = $('#id_class_no').val()
        var team_letter = $('#id_team_letter').val()

        var url = $("#moderate").attr("get-teams-url")
        $.ajax({
            url: url,
            data: {
                'class_no': class_no,
                'team_letter': team_letter,
                'phase': chosen_phase
            },
            success: function(data) {
                $("#dynamic_table").html(data)
            }

        })
        return false;
    })



});