'use strict';

/**
 * @ngdoc function
 * @name webappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the webappApp
 */
angular.module('homeMonitor')
  .controller('MainCtrl', function ($scope, $ardyh) {
      $scope.page = 'main';
      $scope.messages = [];
      $scope.wtf = {'data': null};

      $scope.groveBots = [
          {
              "name": "ardyh/bots/rpi2",
              "location": "Dinning Room",
              "values": {}
          },
          {
              "name": "ardyh/bots/rpi3",
              "location": "Dinning Room",
              "values": {}
          },
          {
              "name": "ardyh/bots/rpi1",
              "location": "Bloom Chamber",
              "values": {}
          }
      ]

      $scope.rpi1 = {'values': $ardyh.bots.rpi1.values};

  });
