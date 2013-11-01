bublController = function ($scope) {
	$scope.BublImage = function (props) {
		var id =  $scope.BublImage.newId();
		for (var prop in props) {
			this[prop] = props[prop];
		}
		this.id = function () {
			return id;
		};
		$scope.BublImage.list.push(this);
	};
	$scope.BublImage.list = [];
	$scope.BublImage.last_id = 346243;
	$scope.BublImage.newId = function () {
		$scope.BublImage.last_id += 1;
		return $scope.BublImage.last_id;
	};
	$scope.BublImage.prototype.getSrc = function () {
		if ($('#' + this.id()).width() > this.thumb.width * 1.2 || this.isFullSize) {
			return this.fullsize.url;
		}
		return this.thumb.url;
	};
	$scope.BublImage.prototype.showFull = function () {
		for (var i = 0; i< $scope.BublImage.list.length; i += 1) {
			if ($scope.BublImage.list[i].isFullSize) {
				$scope.BublImage.list[i].hideFull();
			}
		}
		this.isFullSize = true;
		$('#' + this.id()).addClass('full-size').height($scope.device_height)
		.children('img').css({maxHeight: ($scope.device_height - 40) + 'px'});
		var id = this.id();
		setTimeout(function () {
			location.hash = '';
			location.hash = id;
		}, 30);
		$('#style').html('.image-bubl:nth-of-type(4n+7) {margin-left: 0px;}');
	};
	$scope.BublImage.prototype.hideFull = function () {
		$('#' + this.id()).removeClass('full-size');
		this.isFullSize = false;
		$('#style').html('.image-bubl:nth-of-type(4n+6) {margin-left: 0px;}');
	};
	$scope.BublImage.prototype.toggleFull = function () {
		if (this.isFullSize) {
			this.hideFull();
		}
		else {
			this.showFull();
		}
	};


	$scope.tick = function () {
		$scope.device_height = $('html').height();
		$scope.$apply();
	};
	$scope.tick = setInterval($scope.tick, 500);
	test($scope);
}
var test = function ($scope) {
	$scope.images = [];

	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-frc3/983955_10152952929010704_584207483_n.jpg'
		},
		thumb: {
			width: 309,
			url: 'https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-frc3/p206x206/983955_10152952929010704_584207483_n.jpg'
		},
		title: 'Giving Matt a lift',
		votes: 3});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-frc3/983955_10152952929010704_584207483_n.jpg'
		},
		thumb: {
			width: 309,
			url: 'https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-frc3/p206x206/983955_10152952929010704_584207483_n.jpg'
		},
		title: 'Giving Matt a lift',
		votes: 1});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-frc3/11461_10152952918865704_1778815460_n.jpg'
		},
		thumb: {
			width: 309,
			url: 'https://fbcdn-sphotos-c-a.akamaihd.net/hphotos-ak-prn1/p206x206/11461_10152952918865704_1778815460_n.jpg'
		},
		title: 'The hats come out',
		votes: 4});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-frc3/11461_10152952918865704_1778815460_n.jpg'
		},
		thumb: {
			width: 309,
			url: 'https://fbcdn-sphotos-c-a.akamaihd.net/hphotos-ak-prn1/p206x206/11461_10152952918865704_1778815460_n.jpg'
		},
		title: 'The hats come out',
		votes: 1});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/1013887_10152952903775704_1429897570_n.jpg'
		},
		thumb: {
			width: 206,
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/p206x206/1013887_10152952903775704_1429897570_n.jpg'
		},
		title: 'Being silly',
		votes: 2});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/1013887_10152952903775704_1429897570_n.jpg'
		},
		thumb: {
			width: 206,
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/p206x206/1013887_10152952903775704_1429897570_n.jpg'
		},
		title: 'Being silly',
		votes: 2});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/1013887_10152952903775704_1429897570_n.jpg'
		},
		thumb: {
			width: 206,
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/p206x206/1013887_10152952903775704_1429897570_n.jpg'
		},
		title: 'Being silly',
		votes: 2});
	new $scope.BublImage({	
		fullsize: {
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/1013887_10152952903775704_1429897570_n.jpg'
		},
		thumb: {
			width: 206,
			url: 'https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-prn1/p206x206/1013887_10152952903775704_1429897570_n.jpg'
		},
		title: 'Being silly',
		votes: 2});
}