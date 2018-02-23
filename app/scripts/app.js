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

JumperLQ.config(function($routeProvider, $locationProvider) {
  $routeProvider.when('/', {
    controller : 'LoginController',
    templateUrl: '/partials/login.html',
  });
  $routeProvider.when('/main', {
    controller : 'MainController',
    templateUrl: '/partials/main.html',
  });
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});

JumperLQ.config(function($httpProvider) {
  $httpProvider.interceptors.push('myHttpInterceptor');
});

JumperLQ.run([function($rootScope) {
    window.fbAsyncInit = function() {
    FB.init({
      appId      : '151685772163089',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.12'
    });

    FB.AppEvents.logPageView();

  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));
}]);
