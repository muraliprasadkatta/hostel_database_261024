// for side bar 
// JQUARY CDN LINES
// copy from google 

$(document).ready(function(){
    //jquary for expand and collaps for the sidebar
    $('.menu-btn').click(function(){
       $('.side-bar').addClass('active');
       $('.menu-btn').css("visibility","hidden");
    });
    //for close button
    $('.close-btn').click(function(){
        $('.side-bar').removeClass('active');
        $('.menu-btn').css("visibility","visible");
    });
    //jquary for toggle sub menu
    $('.sub-btn').click(function(){
        $(this).next('.sub-menu').slideToggle();
        $(this).find('.dropdown').toggleClass('rotate');
    });
})
