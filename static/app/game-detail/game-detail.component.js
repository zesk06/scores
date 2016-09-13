'use strict';

// Register `gameDetail` component, along with its associated controller and template
angular.
  module('gameDetail').
  component('gameDetailComponent', {
    bindings: { gameId: '<' },
    templateUrl: 'static/app/game-detail/game-detail.template.html',
    controller: ['GameResource',
      function PhoneDetailController(GameResource) {
        var self = this;
        GameResource.get({ gameId: self.gameId }, function (game) {
          self.setGame(game);
        });

        self.setGame = function setGame(game) {
          self.game = game;
        };
      }
    ]
  });
