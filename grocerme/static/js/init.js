// (function($){
//   $(function(){

    

//   }); // end of document ready
// })(jQuery); // end of jQuery name space

$(document).ready(function() {
	
	$('.button-collapse').sideNav();

	setGoTop();
	toggleGoTop();
	buildContents();


	var caloriesData = 85;
	var sodiumData = 85;
	var sugarData = 85;
	
	var opt = {
		horBarHeight: 30,
		foreColor: '#9ccc65',
		horLabelPos:'right'
	}
	var delay = 1000;

	$('#caloriesBar').barIndicator(opt);
	$('#sodiumBar').barIndicator(opt);
	$('#sugarBar').barIndicator(opt);
	
	setTimeout(function() {
		$('#caloriesBar').barIndicator('loadNewData', [caloriesData]);
		$('#sodiumBar').barIndicator('loadNewData', [sodiumData]);
		$('#sugarBar').barIndicator('loadNewData', [sugarData]);
	}, delay)
	$('#caloriesBar').barIndicator(opt);
});

var buildContents = function() {
	var optHolder = $('#cont-options');
	var methodHolder = $('#cont-methods');
	var eventHolder = $('#cont-events');
	
	$('.secOpt').each(function() {
		var that = $(this);
		var id = that.attr('id');
		var txt = that.attr('data-content');
		optHolder.append('<a class="contAnchor" href="#' + id + '">' + txt + '</a>');
	});
	$('.secMethods').each(function() {
		var that = $(this);
		var id = that.attr('id');
		var txt = that.attr('data-content');
		methodHolder.append('<a class="contAnchor" href="#' + id + '">' + txt + '</a>');
	});
	$('.secEvents').each(function() {
		var that = $(this);
		var id = that.attr('id');
		var txt = that.attr('data-content');
		eventHolder.append('<a class="contAnchor" href="#' + id + '">' + txt + '</a>');
	});
}

var setGoTop = function() {
	var gt = $('#goTop');
	var w = $(window).width();
	var mw = $('#main-wrapper').outerWidth();
	var gtw = gt.outerWidth();
	var r = ((parseFloat(w) - parseFloat(mw)) / 2) - parseFloat(gtw) - 5;
	gt.css({'right': r + 'px'});
}
var toggleGoTop = function() {
	var gt = $('#goTop');
	var t = $(window).scrollTop();
	if (t > 200) {
		gt.show();
	} else {
		gt.hide();
	}
}

$(document).on('click', '#cont-toggle', function() {
	var that = $(this);
	var cont = $('#contents');
	if (cont.hasClass('cont-expanded')) {
		that.html('+');
		cont.removeClass('cont-expanded').addClass('cont-collapsed');
	} else if (cont.hasClass('cont-collapsed')) {
		that.html('-');
		cont.addClass('cont-expanded').removeClass('cont-collapsed');
	}
});

$('#goTop').on('click', function() {
	$('body,html').animate({scrollTop:0},350,'easeOutExpo');	
});

$(window).resize(function() {
	setGoTop();
});
$(window).scroll(function() {
	toggleGoTop();
});

