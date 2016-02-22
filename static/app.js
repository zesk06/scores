var main = function(){
    $('.player-stat .panel-body').hide();
    $('.player-stat-btn').click(function(){
        $(this).parents('.player-stat').find('.panel-body').toggle()
    });
}

$(document).ready(main)
