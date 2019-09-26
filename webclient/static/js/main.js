var app = angular.module('bookingapp', [
  'ui.router',
  'satellizer'
]);

app.constant('URLS', {
  'base': '/api/',
  'register': 'register/',
  'conversation_list': 'conversations/',
  'message_list': 'messages/',
  'message_detail': 'message/',
  'book': 'book/',
})

app.config(function($stateProvider, $urlRouterProvider, $authProvider, $httpProvider){
	$stateProvider
		.state('register', {
			url: '/',
			templateUrl: '/static/templates/register.html',
      controller: 'RegisterCtrl',
      data: {loggedIn: false}
		})
		.state('properties', {
			url: '/properties',
			templateUrl: '/static/templates/properties.html',
      controller: 'PropertiesCtrl',
      data: {loggedIn: true}
    })
    .state('bookings', {
      url: '/bookings',
      templateUrl: '/static/templates/bookings.html',
      controller: 'BookingsCtrl',
      data: { loggedIn: true }
    });

  $urlRouterProvider.otherwise('/');
  $authProvider.tokenType = 'JWT';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


app.controller('RegisterCtrl', function($scope, AuthService, $state, $auth, UserData){
  $scope.username = ''
  $scope.register = function(){
    AuthService.register($scope.username).then(
      function(res){        
        if (res.status == 201){
          console.log(res);
          $auth.setToken(res.data.token);  
          UserData.setId(res.data.user_id)
          $state.go('properties')
        }
      }
    )
  }  
})

app.controller('BookingsCtrl', function($rootScope, $state, $scope, BookingService, UserData){
  $rootScope.browserable = $state.current.data.loggedIn
  BookingService.getBookings(UserData.getId()).then(function(response) {
    $scope.bookings = response.data;
  });
})

app.controller('PropertiesCtrl', function ($rootScope, $scope, $state, BookingService, $http){
  $rootScope.browserable = $state.current.data.loggedIn
  // debugger
  $scope.accomodations = [];
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position){
      $scope.$apply(function(){
        lat = position.coords.latitude
        long = position.coords.longitude
        $http.get('https://places.demo.api.here.com/places/v1/discover/explore;context=Y2F0PWFjY29tbW9kYXRpb24mZmxvdy1pZD03OGVmNzFjNy04YmJlLTU0N2UtYTQ2Yi0zNTE3YTNmYWIxZjNfMTU2ODU3MTg1ODE0OF8wXzcyMTgmb2Zmc2V0PTAmc2l6ZT0yMA?at=' + lat + ',' + long + '&app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg')
        .then(function (response) {
          $scope.accomodations = response.data.items;
        });
      });
    });
  }

  $scope.book = function (accomodation) {
    $http.get('https://places.demo.api.here.com/places/v1/places/' + accomodation.id + ';context=Zmxvdy1pZD0yNDg1ZDY2MS0wODdjLTU4ZjItOTJiNS01MTFlZTA1ZmMxMzVfMTU2OTQ0MzMwNTQ3Nl8wXzkwNTImc2l6ZT01JlgtRldELUFQUC1JRD1EZW1vQXBwSWQwMTA4MjAxM0dBTCZYLU5MUC1UZXN0aW5nPTE?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg')
    .then(function(response){
      BookingService.book(
        { 
          property: { property_id: accomodation.id, property_name: accomodation.title, city: response.data.location.address.city }
        }
      ).then(function () { $state.go('bookings')});
    })
 
  }
})

app.service('UserData', function(){
  var UserData = {}
  UserData.setId = function(userId){
    window.localStorage['userId'] = JSON.stringify(userId);
  }
  UserData.getId = function(){
    return angular.fromJson(window.localStorage['userId']);
  }
  return UserData
})

app.service('AuthService', function($http, URLS){
  var Auth = {};
  REGISTER_URL = URLS.base + URLS.register  
  Auth.register = function(username){
    return $http.post(REGISTER_URL, {'username': username})
  }
  return Auth;
})

app.service('BookingService', function($http, URLS){
  let Booking = {};
  const BOOK_URL = URLS.base + URLS.book

  Booking.book = function(details){
    return $http.post(BOOK_URL, details)
  }
  Booking.getBookings = function(userId){
    return $http.get(URLS.base + 'users/' + userId + '/bookings/')
  }
	return Booking;
});

app.run(function ($rootScope, $state, $auth) {
  $rootScope.$on('$stateChangeStart',
    function (event, toState) {
      var loggedIn = false;
      if (toState.data && toState.data.loggedIn){
        loggedIn = toState.data.loggedIn;      
      }
      if (loggedIn && !$auth.isAuthenticated()) {
        event.preventDefault();
        $state.go('register');
      }
      else if (!loggedIn && $auth.isAuthenticated()) {
        event.preventDefault();
        $state.go('properties');
      }
    });
});