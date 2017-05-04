"use strict";

// Register `gameDetail` component, along with its associated controller and template
angular.module("gameDetail").component("gameDetailComponent", {
  bindings: { gameId: "<" },
  templateUrl: "static/app/game-detail/game-detail.template.html",
  controller: [
    "GameResource",
    function PhoneDetailController(GameResource) {
      var self = this;
      GameResource.get({ gameId: self.gameId }, function(game) {
        self.setGame(game);
      });

      self.setGame = function setGame(game) {
        self.game = game;
        // update charts data
        self.chartScoresByNumberData = [];
        self.chartScoresByNumberLabels = [];
        self.chartScoresByNumberSeries = [];
        self.chartScoresByNumberOptions = {
          title: {
            display: true,
            text: "Score par nombre de joueurs"
          },
          scales: {
            xAxes: [
              {
                ticks: {
                  fixedStepSize: 1,
                  min: 0
                }
              }
            ],
            yAxes: [
              {
                ticks: {
                  suggestedMin: 0
                }
              }
            ]
          }
        };

        for (var player_nb in game.scores_per_number) {
          self.chartScoresByNumberSeries.push(player_nb);
          var datasArray = [];
          var scores = game.scores_per_number[player_nb];
          for (var index in scores) {
            datasArray.push({
              x: player_nb,
              y: scores[index],
              r: 5
            });
          }
          self.chartScoresByNumberData.push(datasArray);
        }
      };
    }
  ]
});
