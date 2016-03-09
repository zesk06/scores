var main = function(){
    $('.date-btn').click(function (){
        // Dates in javascript is fun, to tostring method?
        var today = new Date();
        var curr_date =  today.getDate();
        if (curr_date < 10){
            curr_date = '0' + curr_date;
        }

        var curr_month = today.getMonth() + 1; //Months are zero based
        if (curr_month < 10){
            curr_month = '0' + curr_month;
        }

        var curr_year =  today.getFullYear();
        if (curr_year > 2000){
            curr_year = curr_year - 2000;
        }
       $('#dateId').val(curr_date+'/'+curr_month+'/'+curr_year);
    });

    $('.game-btn').click(function(){
        game_name = $(this).text();
        $('#gameId').val(game_name);
    })

     $('.player-btn').click(function(){
        player_name = $(this).text();
        prev_value = $('#playersId').val()
        if (prev_value === ""){
            $('#playersId').val(player_name+':000');
        }else{
            $('#playersId').val(prev_value + '\n'+player_name+':000');
        }
    })
}

$(document).ready(main)
