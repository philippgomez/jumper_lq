JumperLQ.controller('MainController', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.getUserInfo = function() {
    postData = {
      user_id : $rootScope.user_id
    }
    config = { }
    if (typeof $scope.login_user == "undefined") {
	$scope.login_user = { }
    }

    $http.post('/rest/user', postData, config
        ).success(function(data, status, headers, config) {
          $scope.login_user.first_name = data['first_name']
          $scope.login_user.email = data['email']
          $scope.login_user.cover = data['cover']
        }).error(function(data, status, headers, config) {
        });
  }; 

  $scope.updateUserGroups = function() {
    postData = {
      user_id: $rootScope.user_id
    }
    config = { }

    if (typeof $scope.login_user == "undefined") {
	$scope.login_user = { }
    }

    $http.post('/rest/group', postData, config
        ).success(function(data, status, headers, config) {
          $scope.login_user.groups = data
        }).error(function(data, status, headers, config) {
          $scope.login_user.groups = []
        });
  };

  $scope.getUserInfo();
  $scope.updateUserGroups();

});

