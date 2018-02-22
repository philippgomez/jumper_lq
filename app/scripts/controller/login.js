JumperLQ.controller('LoginController', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.statusChangeCallback = function(response) {
    $rootScope.status = "Processing response ..."
    var token = FB.getAuthResponse()['accessToken']

      FB.api('/me', function(response) {
        var postData = { access_token : token }
        var config = { }

        $http.post('/rest/fbconnect', postData, config
        ).success(function(data, status, headers, config) {
          $scope.login_user.token = data['token']
          $scope.login_user.first_name = data['first_name']
          $rootScope.status = ""
          $location.path("/")
        }).error(function(data, status, headers, config) {
        });
      });
  };

  window.checkLoginState = function() {
    $rootScope.status = "Checking login state ..."
    FB.getLoginStatus(function(response) {
      $scope.statusChangeCallback(response);
    });
  };

});

