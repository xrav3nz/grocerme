$(document).ready(function(){
	// fixes the search bar
    $('.search-wrapper .section').pushpin({ top: $('.search-wrapper').offset().top });
    console.log("potato");
    $.ajax({ 
        type: 'GET', 
        url: '/api/recipes', 
        // data: { get_param: 'results' }, 
        success: function (data) { 
	        for (var i=0;i<data.length;++i){
	        	$('#receipeCard').append(
	        		'<div class="col s6 m4 l3"> \
						<div class="card"> \
							<div class="card-image"> \
								<img src="' + data[i].img_url + '"> \
							</div> \
						<div class="card-content"> \
			    			<span class="card-title activator grey-text text-darken-4">' + data[i].title+ '</span> \
			    		</div> \
					</div> \
				</div>');
	        }
        }
    });

});

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


