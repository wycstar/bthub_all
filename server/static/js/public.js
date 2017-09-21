$(document).ready(function(){
    let hs = $("#hot-search");
    $(document).scroll(function(event) {
        if(($(document.body).scrollTop() + $(document.documentElement).scrollTop()) > 25){
            hs.addClass("hot-search-fixed");
            hs.offset({left:hs.offset().left});
        }
        else if($(document.body).scrollTop() <= 25){
            hs.removeClass("hot-search-fixed")
        }
    });
});