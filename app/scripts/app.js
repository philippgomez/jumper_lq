'use strict';

var JumperLQ = angular.module('JumperLQ', ['ngRoute']);

JumperLQ.factory('myHttpInterceptor', function($rootScope, $q) {
  return {
    'requestError': function(config) {
      $rootScope.status = 'HTTP REQUEST ERROR ' + config;
      return config || $q.when(config);
    },
    'responseError': function(rejection) {
      $rootScope.status = 'HTTP RESPONSE ERROR ' + rejection.status + '\n' +
                          rejection.data;
      return $q.reject(rejection);
    },
  };
});

JumperLQ.config(function($routeProvider) {
  $routeProvider.when('/', {
    controller : 'LoginController',
    templateUrl: '/partials/login.html',
  });
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});

JumperLQ.config(function($httpProvider) {
  $httpProvider.interceptors.push('myHttpInterceptor');
});

}

