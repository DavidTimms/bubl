$(document).ready(function () {

	// Hide and show the upload form
	var upload_form = $('.upload-form').hide();
	$('.add-image-btn').click(function () {
		upload_form.slideToggle();
	});

	// switch between adding by file and by URL
	$('.url-input').hide();
	$('.type-select').click(function (event) {
		var selection = $(this).attr('value');
		var selectors = {url: '.url-input', file: '.file-input'};
		for (var x in selectors) {
			if (x === selection)
				$(selectors[x]).show();
			else 
				$(selectors[x]).hide();
		}
	});

	// Control the file upload input
	var upload_input = $('.file-upload');
	var dummy_input = $('.file-input');
	$('.file-input').click(function (event) {
		upload_input.click();
	});
	upload_input.on('change', function (event) {
		var filename = this.value.split(/\\|\//).pop();
		dummy_input.html(filename);
	});
	
	var bubl_boxes = $('.image-bubl');
	// upvote and downvote
	bubl_boxes.on('click', '.upvote, .downvote', function (event) {
		var self = $(this);
		event.preventDefault();
		var image_id = self.closest('.image-bubl').attr('id');

		var alter_score = function (amount) {
			var score_node = self.closest('.vote-buttons')
								.find('.score');
			var score = Number(score_node.html());
			score_node.html(score + amount);
		}

		var deactivate = function (classname) {
			var other = self.closest('.vote-buttons')
							.find('.' + classname);
			var active = other.hasClass('active');
			other.removeClass('active');
			return active;
		}

		var vote_type;
		if (self.hasClass('upvote')) {
			vote_type = 'up';
			if (self.hasClass('active'))
				alter_score(-1);
			else if (deactivate('downvote'))
				alter_score(2);
			else
				alter_score(1);
		}
		else {
			vote_type = 'down';
			if (self.hasClass('active'))
				alter_score(1);
			else if (deactivate('upvote'))
				alter_score(-2);
			else
				alter_score(-1);
		}
		self.toggleClass('active');

		$.post('/vote', {
			'vote_type': vote_type,
			'image_id': image_id
		}).always(function (res) {
			console.log(res);
		});
	});

	var confirm_delete_template = $('.confirm-delete-template').html();
	$('.confirm-delete-template').remove();
	bubl_boxes.on('click', '.delete-image', function (event) {
	//$('.delete-image').click(function (event) {
		event.preventDefault();

		var container = $(this).closest('.image-bubl');
		var link = container.find('a');
		var height = container.height();
		var confirm_box = $('<div></div>')
			.css('height', height + 'px')
			.css('padding-top', height/2 + 'px')
			.addClass('image-bubl')
			.html(confirm_delete_template)
			.insertAfter(container);


		// attach event handlers for the cancel and delete buttons
		confirm_box.find('.cancel-delete').click(function (event) {
			confirm_box.remove();
			container.show();
		});

		confirm_box.find('.confirm-delete').click(function (event) {
			var image_id = container.attr('id');

			// send delete request to server
			$.post(location.pathname + '/delete_image', {
				'image_id': image_id
			}).always(function (res) {
				console.log(res);
			});

			// remove the image and confirm box from the page
			confirm_box.slideUp();
			container.remove();
		});
			
		container.hide();
	});
});