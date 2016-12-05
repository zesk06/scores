'use strict';

// Register `phoneList` component, along with its associated controller and template
angular.
  module('playerList').
  component('playerListComponent', {
    templateUrl: 'static/app/player-list/player-list.template.html',
    controller: ['PlayerResource',
      function playerListController(PlayerResource) {
        var self = this;
        self.plays = [];
        self.orderProp = '-elo';
        PlayerResource.query({playerId:''}, function(players){
            self.setPlayers(players);
        });

        self.setPlayers = function setPlayers(players){
          self.players = players;
          players.forEach(function(player, index, array){
              player.percentage = 100 * player.win / player.plays_number;
              player.percentage = Number(player.percentage.toFixed(0));
              /* group beaten by player name
              { 'lolo':4, 'zesk': 2} */
              var countBy = _.countBy(player.beaten_by);
              /*transform map to array [['lolo',4], ['zesk', 4]]*/
              var pairs = _.toPairs(countBy);
              /* and retrieve the max */
              player.worst_ennemy = _.maxBy(pairs,function(o){return o[1]});
              /* thx lodash */
          });
        };
      }]
  });
