'use strict';

// Register `gameDetail` component, along with its associated controller and template
angular.
  module('gameDetail').
  component('gameDetail', {
    templateUrl: 'static/app/game-detail/game-detail.template.html',
    controller: ['$routeParams', 'GameResource',
      function PhoneDetailController($routeParams, GameResource) {
        var self = this;

        GameResource.get({gameId: $routeParams.gameId}, function(game) {
          self.setGame(game);
        });

        self.setGame = function setGame(game) {
          self.game = game;
        };
      }
    ]
  });
