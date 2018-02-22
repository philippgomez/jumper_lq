function LoginController($scope, $http) {
  $scope.checkLoginState = function() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  };

  $scope.statusChangeCallback(response) = function() {
    var token = FB.getAuthResponse()['access_token']
    FB.api('/me', function(response) {
      var postData = { access_token : token }
      var config = { }

      $http.post('/rest/fbconnect', postData, config
      ).success(function(data, status, headers, config) {
        $scope.user = data
      }).error(function(data, status, headers, config) {
      });
    }
  };
}
