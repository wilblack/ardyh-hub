'use strict';

/**
 * @ngdoc directive
 * @name homeMonitor.directive:grovebotPanel
 * @description
 * # grovebotPanel
 */
angular.module('homeMonitor')
.directive('grovebotPanel', [ '$rootScope', '$ardyh', function ($rootScope, $ardyh) {
    return {
        templateUrl: 'views/directives/grovebot-panel.html',
        restrict: 'EA',
        scope: {
            botName: "=",
            values: "=",
            location: "="
        },
        link: function postLink(scope, element, attrs) {
            scope.units = {'temp': 'f'};

            $rootScope.$on('ardyh-onmessage', function(e, data){
                if (data.topic !== scope.botName) return;
                scope.$apply(function(){
                    scope.values = data.payload;
                });
            });

            scope.celsius2fahrenheit = function(t){
                return t*(9/5) + 32;
            };

            scope.shutdown = function(botName){
                console.log("[grovebotPanel.shutdown()]");
                $ardyh.sendCommand('shutdown', {'botName':botName });

            };

            scope.restart = function(botName){
                console.log("[grovebotPanel.restart()]");
                $ardyh.sendCommand('restart', {'botName':botName});
            };
        }
    };
}]);
