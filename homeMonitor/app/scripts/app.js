'use strict';

/**
 * @ngdoc overview
 * @name webappApp
 * @description
 * # webappApp
 *
 * Main module of the application.
 */
angular
    .module('homeMonitor', [
        'ngAnimate',
        'ngAria',
        'ngCookies',
        'ngMessages',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'ardyhServices',
        'mockServices',
        'nvd3',
    ])
    .constant('config', {
        "hubDomain": "192.168.0.106:9093"
    })

    .config(function ($routeProvider) {
        $routeProvider
        .when('/', {
            templateUrl: 'views/main.html',
            controller: 'MainCtrl',
            controllerAs: 'main'
        })
        .when('/settings', {
            templateUrl: 'views/settings.html',
            controller: 'SettingsCtrl',
            controllerAs: 'settings'
        })
        .otherwise({
            redirectTo: '/'
        });
  });
