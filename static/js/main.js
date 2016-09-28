
$(document).ready(function(){

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

});



function ResultBox(){
    $('.resultBox').height($('.resultBox').outerWidth());
}

