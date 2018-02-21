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
    controller : 'LoginCtrl',
    templateUrl: '/partials/login.html',
  });
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});

JumperLQ.config(function($httpProvider) {
  $httpProvider.interceptors.push('myHttpInterceptor');
});


function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

function statusChangeCallback(response) {
  var access_token = FB.getAuthResponse()['access_token']
  FB.api('/me', function(response) {
     $.ajax({
      type: 'POST',
      url: '/fbconnect?state=connect',
      processData: false,
      data: access_token,
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        if (result) {
         setTimeout(function() {
         window.location.href = "/group";
         }, 4000);
      } else {
         }
  }
}

