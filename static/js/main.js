
$(document).ready(function(){

    $('#main_search_container').outerWidth(
            $('#form_container').width()
            - ($('.form-group.col-md-6').width() - $('#topic').width())
        );

    if($('#model_type').val() == 'Person'){
       $("input[name='job']").fadeIn();
    }
    if($("#country").val() == "France"){
        $("input[name='zipcode']").fadeIn();
    }

    $('#model_type').change(function(){
        if($(this).val() == "Person"){
            $("input[name='job']").fadeIn();
        }else{
            $("input[name='job']").fadeOut();
        }
    });

    $("#country").change(function(){
        if($(this).val() == "France"){
            $("input[name='zipcode']").fadeIn();
        }else{
            $("input[name='zipcode']").fadeOut();
        }
    });

    $('#topic').change(function(){
        $('select[name="subtopic"]').css('display','none');
        rel = $('#topic option:selected').val();
        target = $('select[name="subtopic"][rel="'+rel+'"]');
        target.fadeIn();
    });

    ResultBox();
    $('#deploy_secondary').click(function(){
        $('#secondary_search_container').addClass('deploy');
        $(this).addClass('hide');
    });

    $('#main_search_input').focus();

    // if($('body').height()<=$(window).height()){
    //     $('footer').css('margin-top',$(window).height()-$('body').height());
    // }
});

$(window).resize(function(){
    $('#main_search_container').outerWidth(
            $('#form_container').width()
            - ($('.form-group.col-md-6').width() - $('#topic').width())
        );
    resultBox();
});


function ResultBox(){
    $('.resultBox').height($('.resultBox').outerWidth());
}

