"use strict";

angular.module("playerDetail").component("playerDetailComponent", {
  bindings: { playerId: "<" },
  templateUrl: "static/app/player-detail/player-detail.template.html",
  controller: [
    "PlayerResource",
    function PlayerDetailController(PlayerResource) {
      var self = this;
      PlayerResource.get({ playerId: self.playerId }, function(player) {
        self.setPlayer(player);
      });

      self.updateGameChart = function(player) {
        /* group games by game name
              { 'ascencion':4, '7wonders': 2} */
        var countBy = _.countBy(player.games);
        self.chartGamesData = [];
        self.chartGamesLabels = _.keys(countBy).sort();
        self.chartGamesColors = [];
        for (var index in self.chartGamesLabels) {
          var gameName = self.chartGamesLabels[index];
          var gameNb = countBy[gameName];
          self.chartGamesData.push(gameNb);
          // We need a colors array as long as the datas
          self.chartGamesColors.push("#90CAF9");
        }

        self.chartGamesOptions = {
          title: {
            display: true,
            text: "Jeux"
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
                  fixedStepSize: 1,
                  suggestedMin: 0
                }
              }
            ]
          }
        };
      };

      self.updateBeatenByChart = function(player) {
        /* group BeatenBy by BeatenBy name
              { 'ascencion':4, '7wonders': 2} */
        var countBy = _.countBy(player.beaten_by);
        self.chartBeatenByData = [];
        self.chartBeatenByLabels = _.keys(countBy).sort();
        self.chartBeatenByColors = [];
        for (var index in self.chartBeatenByLabels) {
          var BeatenByName = self.chartBeatenByLabels[index];
          var BeatenByNb = countBy[BeatenByName];
          self.chartBeatenByData.push(BeatenByNb);
          // We need a colors array as long as the datas
          self.chartBeatenByColors.push("#00BCD4");
        }

        self.chartBeatenByOptions = {
          title: {
            display: true,
            text: "Nemesis scale"
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
                  fixedStepSize: 1,
                  suggestedMin: 0
                }
              }
            ]
          }
        };
      };

      self.setPlayer = function setPlayer(player) {
        self.player = player;
        self.updateGameChart(player);
        self.updateBeatenByChart(player);
      };
    }
  ]
});
