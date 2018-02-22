JumperLQ.controller('MainController', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  FB.getLoginStatus(function(response) {
    if response['status'] != 'connected' :
      $location.path('/login')
  });

  $scope.getUser = function() {
    postData = {
      user_id: login_user.user_id,
    }
    config = { }

    $http.post('/rest/user/', postData, config
        ).success(function(data, status, headers, config) {
          $rootScope.login_user.first_name = data['first_name']
          $rootScope.login_user.token = data['token']
        }).error(function(data, status, headers, config) {
        });
  } 

  $scope.updateUserGroups = function() {
    postData = {
      user_id: login_user.user_id,
      token: login_user.token
    }
    config = { }

    $http.post('/rest/group/', postData, config
        ).success(function(data, status, headers, config) {
          $rootScope.login_user['groups'] = data
        }).error(function(data, status, headers, config) {
          $rootScope.login_user['groups'] = []
        });
  }

  $scope.getUser()
  $scope.updateUserGroups()

});

