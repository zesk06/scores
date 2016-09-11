'use strict';

angular.
  module('scoresApp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');
      $routeProvider.
        when('/plays', {
          template: '<play-list></play-list>'
        }).
        when('/plays/:playId', {
          template: '<play-detail></play-detail>'
        }).
        when('/games/:gameId', {
          template: '<game-detail></game-detail>'
        }).
        otherwise('/plays').
        when('/players/:playerId', {
          template: '<player-detail></player-detail>'
        }).
        otherwise('/plays');
    }
  ]);