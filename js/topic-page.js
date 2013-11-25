$(document).ready(function () {
	var upload_form = $('.upload-form').hide();
	$('.add-image-btn').click(function () {
		upload_form.slideToggle();
	});

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

	var upload_input = $('.file-upload');
	var dummy_input = $('.file-input');
	$('.file-input').click(function (event) {
		upload_input.click();
	});
	upload_input.on('change', function (event) {
		var filename = this.value.split(/\\|\//).pop();
		dummy_input.html(filename);
	});
	
	$('.upvote, .downvote').click(function (event) {
		var self = $(this);
		event.preventDefault();
		var image_id = self.closest('.image-bubl').attr('id');

		var alter_score = function (amount) {
			var score_node = self.closest('.vote-buttons')
								.find('.score sup');
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
});