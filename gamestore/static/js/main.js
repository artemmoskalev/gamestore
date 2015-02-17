$(document).ready(function(){

	/* redirects to the category pages when the game information panel is clicked
	   parses the title of the category image and creates a request path */
	$(".category").click(function(){
		var game_title = $(this).find(".game_title h1").text();
		var category_request = "/games/";
		if(game_title == "Action Games") {
			category_request += "action/";
		} else if(game_title == "Adventures") {
			category_request += "adventure/";
		} else if(game_title == "Sport Games") {
			category_request += "sport/";
		} else if(game_title == "Strategies") {
			category_request += "strategy/";
		} else if(game_title == "Puzzles") {
			category_request += "puzzle/";
		} else {
			category_request += "misc/";
		}
		window.location.href = category_request;
		return false;
	});	
		
	$(".game").click(function() {
		var game_title = $(this).find(".game_title h1").text();
		window.location.href = "/games/" + encodeURIComponent(game_title) + "/";
		return false;
	});
	
    // mobile menu toggling
    $("#menu_icon").click(function(){
        $("header nav ul").toggleClass("show_menu");
        $("#menu_icon").toggleClass("close_menu");        
        return false;
    });

    
    /* Tooltip JavaScript */    
    
    // create a tooltip element
    $(".social a").mouseover(function(){  
    	
        $(this).after('<span class="tooltip"></span>');

        var tooltip = $(".tooltip");
        tooltip.append($(this).data('title'));
         
        var tipwidth = tooltip.outerWidth();
        var a_width = $(this).width();
        var a_hegiht = $(this).height() + 3 + 4;

        // setting the tooltip over the link element
        var tipwidth = '-' + (tipwidth - a_width)/2;
        $('.tooltip').css({
            'left' : tipwidth + 'px',
            'bottom' : a_hegiht + 'px'
        }).stop().animate({
            opacity : 1
        }, 200);       

    });
    // remove tooltip element
    $("a").mouseout(function(){
        var tooltip = $(".tooltip");       
        tooltip.remove();
    });
    
});





