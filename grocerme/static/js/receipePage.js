$(document).ready(function(){
	// fixes the search bar
	var page = 0;
	var key_word = "";
	var endpoint = {
		'recommend': '/api/recipes/recommend',
		'search': '/api/recipes'
	};
	var in_ajax = false;
    $('.search-wrapper .section').pushpin({ top: $('.search-wrapper').offset().top });
    ajaxGet(endpoint.recommend, '', 0, 0);
    $('#recipeSearch').bind('click', function() {
    	$("#seeMore").hide();
    	$("#header1").hide();
    	$("#receipeGen").empty();
    	page = 0;
    	key_word = $("#search").val();
    	ajaxGet(endpoint.search, key_word, 4, page, function() {
    		$('#seeMore').show();
    	});
    	++page;
    });
    $('#seeMore').bind('click', function(e) {
    	e.preventDefault();
    	ajaxGet(endpoint.search, key_word, 4, page);
    	++page;
    })
    $('#receipeGen').on('click', '.card', function() {
    	if (in_ajax) return ;
    	in_ajax = true;
    	var recipe_id = $(this).attr('id');
    	$('#recipeDetails').load('/api/recipes/' + recipe_id, function() {
    		 $('#recipeModal').openModal();
    		 in_ajax = false;
    	});
    })
});

function ajaxGet(endpoint, q, per_page, page, callback) {
	$.ajax({
        type: 'GET',
        url: endpoint,
        data: {'q': q, 'per_page': per_page, 'page': page},
        success: function (data) {
            console.log(data);
            if (data.results.length <= 0) {
            	$('#receipeGen').append('<h6 class="light center-align"> No matches :( </h6>');
            }
	        for (var i = 0; i < data.results.length; ++i) {
	        	$('#receipeGen').append(
	        		'<div class="col s6 m4 l3"> \
						<div class="card" id="' + data.results[i].id + '"> \
							<div class="card-image"> \
								<img style="height: 25%" src="' + data.results[i].img_url + '"> \
							</div> \
							<div class="card-content"> \
			    				<span style="font-size: 18px" class="card-title activator grey-text text-darken-4 truncate">' + data.results[i].title+ '</span> \
			    			</div> \
						</div> \
					</div>');
	        }
	        if (data.results.length > 0 && callback)
		        callback();
        }
    });
}

// function populator() {
// 	ajax->JSON
// 	for object in json:
// 		dom = new_dom(object)
// 		body.append(dom)
// }

// function new_dom() {
// 	return "<>" + dynamic_data + "<>";
// }

//
/*var potato = $(myJSONfile);
var fileReceipe = JSON.parse(potato);

function Receipe(imgUrl, name, content) {
	this.imgUrl = imgUrl;
	this.name = name;
	this.content=content;
}

var listReceipe = [];

for (var item in fileReceipe) {
	tempReceipe = new Receipe(item[0], item[1], item[2]);
	listReceipe.push(tempReceipe);
}*/


