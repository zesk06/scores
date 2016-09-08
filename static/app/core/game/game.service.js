'use strict';

angular.
  module('core.game').
  factory('GameResource', ['$resource',
    // see $resource documentation:
    // https://docs.angularjs.org/api/ngResource/service/$resource
    function($resource) {
      return $resource('api/v1/games/:gameId', {}, {
        get: {
          method: 'GET',
          isArray: false
        }
      });
    }
  ]);
