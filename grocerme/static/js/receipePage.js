$(document).ready(function(){
	// fixes the search bar
	var page = 0;
	var key_word = "";
    $('.search-wrapper .section').pushpin({ top: $('.search-wrapper').offset().top });
    ajaxGet();
    $('#recipeSearch').bind('click', function() {
    	$("#receipeGen").empty();
    	page = 0;
    	key_word = $("#search").val();
    	ajaxGet(key_word, 4, page);
    	++page;
    });
    $('#seeMore').bind('click', function() {
    	ajaxGet(key_word, 4, page);
    	++page;
    })
});

function ajaxGet(q, per_page, page) {
	$.ajax({
        type: 'GET',
        url: '/api/recipes',
        data: {'q': q, 'per_page': per_page, 'page': page},
        success: function (data) {
            console.log(data);
	        for (var i=0;i<data.results.length;++i){
	        	$('#receipeGen').append(
	        		'<div class="col s6 m4 l3"> \
						<div class="card"> \
							<div class="card-image"> \
								<img style="height: 25%" src="' + data.results[i].img_url + '"> \
							</div> \
							<div class="card-content"> \
			    				<span style="font-size: 18px" class="card-title activator grey-text text-darken-4 truncate">' + data.results[i].title+ '</span> \
			    			</div> \
						</div> \
					</div>');
	        }
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


