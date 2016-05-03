'use strict';

/**
 * @ngdoc service
 * @name webappApp.ardyhServices.js
 * @description
 * # ardyhServices.js
 * Service in the webappApp.
 */
angular.module('ardyhServices', [])
.service('$ardyh', function ($rootScope, $q, $http, config) {
    // AngularJS will instantiate a singleton by calling "new" on this function

    console.log('[ardyhServices]');

    var obj = this;
    var DOMAIN = config.hubDomain;
    var SOCKET_URL = "ws://" + DOMAIN + "/ws";
    obj.dtFormat = 'hh:mm:ss tt, ddd MMM dd, yyyy';

    console.log("opening socket connection to " + SOCKET_URL + "?homeMonitor");

    obj.socket = new WebSocket(SOCKET_URL);


    obj.socket.onopen = function(){
        console.log("connection opened....");
        $rootScope.$broadcast('ardyh-onopen');
        var handshake = {"text": "Hello from the browser"};
        var out = JSON.stringify(handshake);
        obj.socket.send(out);
    };

    obj.socket.onmessage = function(msg) {
        /*
            msg should have a JSON string at msg.data.

            data should have keywords 'topic' and 'payload'
        */
        try {
            var data = JSON.parse(msg.data);
        } catch(e) {

            console.log("['onmessage'] Could parse, gonna try replacing NaN's", msg);
            var tmp = msg.data.replace(/NaN/g, 'null');
            var data = JSON.parse(tmp);
        }

        $rootScope.$broadcast('ardyh-onmessage', data);
    };

    obj.socket.onclose = function(){
        //alert("connection closed....");
        console.log("The connection has been closed.");
        $rootScope.$broadcast('ardyh-onclose');
    };

    obj.socket.onerror = function(e){
        console.log("The was an error.", e);
        $rootScope.$broadcast('ardyh-onerror', e);

    };


    obj.send = function(messageObj) {
        if (obj.socket.readyState === 1){
            obj.socket.send(JSON.stringify( messageObj));
        } else {
            console.log("Could not send message, ready state = "+obj.socket.readyState);
            if (obj.socket.readyState === 3){
                // Web socket is closed so try to re-establish connection
                console.log("I should reconnect here.");
                $timeout(function(){
                    obj.init(obj.botName);
                }, 5*1000);
            }
        }
    };

    obj.sendCommand = function(command, kwargs){
        kwargs = kwargs || {};
        obj.send({'command':command, 'kwargs':kwargs});
    }

    obj.bots = {};

    obj.bots.rpi1 = {
        botName: "ardyh/bots/rpi1",
        values: [],
    };

    obj.fetchValues = function(botName, start, end){
        var defer = $q.defer();
        botName = angular.copy(botName).replace( new RegExp("/", 'g'), ".");

        var url = "http://" + DOMAIN + "/api/sensors/" + botName;

        if (end){
            url += "?end=" + end;
        } else {
            url += "?end=-120";
        }

        if (start){
            url += "&start=" + start;
        };

        $http.get(url)
            .then(function(data, status){
                defer.resolve(data.data, status);
            }, function(data, status){
                console.log(status);
                console.log(data);
                defer.reject(data, status);
            });
        return defer.promise;
    }
});
