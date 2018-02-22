JumperLQ.controller('LoginController', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.statusChangeCallback = function(response) {
    $rootScope.status = "Processing response ..."
    var token = FB.getAuthResponse()['access_token']

    FB.api('/me', function(response) {
      var postData = { access_token : token }
      var config = { }

      $http.post('/rest/fbconnect', postData, config
      ).success(function(data, status, headers, config) {
        $scope.user = data
        $rootScope.status = ""
      }).error(function(data, status, headers, config) {
      });
    });
  };

  $scope.checkLoginState = function() {
    $rootScope.status = "Checking login state ..."
    FB.getLoginStatus(function(response) {
      $scope.statusChangeCallback(response);
    });
  };


});

