angular.module('mockServices', [])
.service('$mockArdyh', ['$rootScope', '$interval', function ($rootScope, $interval) {
    window.setInterval(function(){
        data = {
            "temp": Math.random().toFixed(2),
            "humidity": (Math.random() * 100).toFixed(2),
            "light": (Math.random() *1000).toFixed(2)
        };
        $rootScope.$broadcast('ardyh-onmessage', data);
    }, 1000);
}]);
