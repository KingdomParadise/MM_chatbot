



// $(window).on('',function(e){
//     if($(window).width()<800){$('#col1').addClass('m12')}
//     else{$('#col1').removeClass('m12')}
// })

$(window).on('resize load',function(e){
    if($(window).width()<600){$('.sidenav-fixed').css('margin-top','55px')}
    else{$('.sidenav-fixed').css('margin-top','65px')}
}) 

// $(window).on('load',function(e){
//     if($(window).width()<600){$('.sidenav-fixed').css('margin-top','55px')}
//     else{$('.sidenav-fixed').css('margin-top','65px')}
// }) 

$(window).on('load resize',function(e){
    if($(window).width()<=976){
        $('.sub_sidebar_activator').css('display','block')
        // $('.navigator_btns').css('display','none')

    }
    else{
        $('.sub_sidebar_activator').css('display','none') 
    }
}) 

 
// $(window).on('resize',function(e){
//     if($(window).width()<580){
//         $('.navigate').css('width','100%')
//         $('.navigate').css('margin-bottom','10px')
//     }
//     else{$('.navigate').css('width','auto')}
  
// })
// $(window).on('load',function(e){
//     if($(window).width()<580){
//         $('.navigate').css('width','100%')
//         $('.navigate').css('margin-bottom','10px')
//     }
//     else{$('.navigate').css('width','auto')}
  
// })