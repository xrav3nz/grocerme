function FridgeItem(item) {
	this.item_name = ko.observable();
	this.quantity = ko.observable();
	this.unit_id = ko.observable();
	this.expiry_date = ko.observable();
	this.expire_note = ko.observable();

	this.id = item.id;
	this.item_name(item.name);
	this.quantity(item.quantity);
	this.unit_id(item.unit);
	this.expiry_date(item.expiry_date);
	var date_obj = moment(item.expiry_date);
	if (moment().diff(date_obj) < 0) {
		this.expire_note("Expires in " + date_obj.toNow(true));
	} else {
		this.expire_note("Expired for " + date_obj.toNow(true));
	}
	this.expiry_time = date_obj.format("x");
}

function Unit(unit) {
	this.name = unit.name;
	this.abbr = unit.abbr;
	this.id = unit.id;
}

function getAllUnits() {
	var self = this;

	self.units = ko.observableArray([]);

	$.getJSON("/api/units", function(data) {
	    var result = $.map(data, function(unit) { return new Unit(unit) });
	    self.units(result);
	});
}

// This is a simple *viewmodel* - JavaScript that defines the data and behavior of your UI
function FridgeViewModel() {
	var self = this;

	self.selectedUnit = ko.observable();
	self.fridgeItems = ko.observableArray([]);

	self.editItemName = ko.observable();
	self.editItemQuantity = ko.observable();
	self.editItemUnit = ko.observable();
	self.editItemExpiryDate = ko.observable();
	self.editItemId = ko.observable();

	self.newItemName = ko.observable();
	self.newItemQuantity = ko.observable();
	self.newItemUnit = ko.observable();
	self.newItemExpiryDate = ko.observable();

	self.addItem = function() {
		var newItem = {
			item_name: self.newItemName(),
			quantity: self.newItemQuantity(),
			unit_id: self.selectedUnit().id,
			expiry_date: moment(self.newItemExpiryDate()).format("YYYY-MM-DD HH:mm:SS")
		};
		console.log(newItem);
		$.ajax({
			url: '/api/fridges',
			data: newItem,
			type: 'POST',
			success: function(result) {
				console.log(JSON.parse(result));
				self.fridgeItems.push(new FridgeItem(JSON.parse(result)));
				sortFridgeItems();
			}
		});
	}


	function sortFridgeItems() {
		self.sortedFridgeItems = ko.computed(function(){
			return self.fridgeItems().sort(function(l, r){ 
				return l.expiry_time == r.expiry_time ? 
				(l.item_name().toLowerCase() < r.item_name().toLowerCase() ? -1 : 1) : 
				(l.expiry_time < r.expiry_time ? -1 : 1) 
			});
		});
	}

	self.getAllItems = function() {

		$.getJSON("/api/fridges/all", function(data) {
		    // Now use this data to update your view models,
		    // and Knockout will update your UI automatically
		    var result = $.map(data.items, function(item) { return new FridgeItem(item) });
		    self.fridgeItems(result);
		});
	}

	self.removeItem = function(item) {
		$.ajax({
			url: '/api/fridges/' + item.id,
			type: 'DELETE',
			success: function(result) {
				console.log(item);
				Materialize.toast('Removed one item from fridge!', 4000)
				self.fridgeItems.remove(item);
			}
		});
	};

	self.editItem = function(item) {
		self.editItemId(item.id);
		self.editItemName(item.item_name());
		self.editItemUnit(item.unit_id());
		self.editItemQuantity(item.quantity());
		var expiry_date = moment(item.expiry_time, "x").format("D MMMM, YYYY");
		self.editItemExpiryDate(expiry_date);
		$('#edit-item-modal').openModal();
	};

	self.saveEditedItem = function() {
		var editItem = {
			id: self.editItemId(),
			item_name: self.editItemName(),
			quantity: self.editItemQuantity(),
			unit_id: self.editItemUnit().id,
			expiry_date: moment(self.editItemExpiryDate()).format("YYYY-MM-DD HH:mm:SS")
		};
		$.ajax({
			data: editItem,
			url: '/api/fridges/' + editItem.id,
			type: 'PUT',
			success: function(result) {
				var tmp = new FridgeItem(JSON.parse(result));
				var index = self.sortedFridgeItems().findIndex(function(element, index, array){
					return element.id === tmp.id;
				});
				self.sortedFridgeItems()[index].item_name(tmp.item_name());
				self.sortedFridgeItems()[index].unit_id(tmp.unit_id());
				self.sortedFridgeItems()[index].quantity(tmp.quantity());
				self.sortedFridgeItems()[index].expiry_date(tmp.expiry_date());
				self.sortedFridgeItems()[index].expire_note(tmp.expire_note());
			}
		});
	};

	self.getAllItems();
	sortFridgeItems();
	getAllUnits();

}

// Activates knockout.js
ko.applyBindings(new FridgeViewModel());


$(document).ready(function() {

	$('.datepicker').pickadate({
		selectMonths: true, // Creates a dropdown to control month
		selectYears: 15 // Creates a dropdown of 15 years to control year
	});

	// the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();

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

