JumperLQ.controller('MainController', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  FB.getLoginStatus(function(response) {
    if response['status'] != 'connected' :
      $location.path('/login')
  });

});

