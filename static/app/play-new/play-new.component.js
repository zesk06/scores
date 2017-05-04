"use strict";

angular.module("playNew").component("playNewComponent", {
  bindings: { playId: "<", action: "<" },
  templateUrl: "static/app/play-new/play-new.template.html",
  controller: [
    "PlayResource",
    "GameResource",
    "PlayerResource",
    "$http",
    function PlayNewController(
      PlayResource,
      GameResource,
      PlayerResource,
      $http
    ) {
      var self = this;
      // An object to retrieve the form values
      self.date_s = new Date();
      self.time_s = new Date();
      self.time_s.setSeconds(0);
      self.time_s.setMilliseconds(0);
      self.infos = [];
      self.warnings = [];
      self.added_plays = [];

      // The new player default values
      self.new_player = {
        login: "",
        score: 0,
        color: "",
        role: "",
        team: "",
        team_color: ""
      };
      // the available player logins
      self.logins = [];
      // The selected login to add a new player
      self.login = self.logins[0];
      // the available games
      self.games = [];
      //the available players
      self.players = [];

      // an index to autoname players
      self.player_index = 0;
      self.initFields = function(play) {
        self.fields = {
          game: "",
          date: 0,
          wintype: "max",
          comment: "",
          players: [],
          winners: [],
          winners_reason: []
        };
        if (play) {
          self.fields._id = play._id;
          self.fields.game = play.game;
          self.fields.wintype = play.wintype;
          self.fields.comment = play.comment;
          self.fields.players = play.players;
          self.fields.winners = play.winners;
          self.fields.winners_reason = play.winners_reason;
          // We must create new date here, to have
          // HTML angular model be notified of the date change
          self.date_s = new Date();
          self.time_s = new Date();
          var gameDate = new Date(play.date);
          self.date_s.setDate(gameDate.getDate());
          self.date_s.setMonth(gameDate.getMonth());
          self.date_s.setYear(gameDate.getFullYear());
          self.time_s.setHours(gameDate.getHours());
          self.time_s.setMinutes(gameDate.getMinutes());
          self.time_s.setSeconds(0);
          self.time_s.setMilliseconds(0);
        }
      };
      self.addPlayer = function(login) {
        var player = JSON.parse(JSON.stringify(self.new_player));
        if (login) {
          player.login = login;
        }
        if (player.login === "player") {
          player.login = "player_" + self.player_index;
        }
        player.index = self.player_index;
        self.fields.players.push(player);
        self.player_index += 1;
      };

      self.removePlayer = function(player) {
        for (var index in self.fields.players) {
          if (self.fields.players[index].index === player.index) {
            self.fields.players.splice(index, 1);
          }
        }
      };

      self.setGame = function(game) {
        self.fields.game = game;
      };

      self.getGames = function() {
        self.games = GameResource.query();
      };

      self.getPlayers = function() {
        self.players = PlayerResource.query();
      };
      /**
                 * Return the id of the given play
                 */
      self.getPlayId = function getPlayId(play) {
        return play._id["$oid"];
      };

      self.isLogged = function() {
        return document.user_is_logged;
      };

      self.submitMyForm = function() {
        /* while compiling form , angular created this object*/
        self.warnings = [];
        self.infos = [];
        // clone the data object, so we can change values
        var data = JSON.parse(JSON.stringify(self.fields));
        //convert the date to a timestamp
        var gameDate = new Date(self.date_s);
        if (self.time_s) {
          gameDate.setHours(self.time_s.getHours(), self.time_s.getMinutes());
        }
        data.date = gameDate.getTime();
        if (data.players.length == 0) {
          self.warnings.push("Game must have at least one player!");
        }
        if (data.game.length == 0) {
          self.warnings.push("Game name must not be empty!");
        }
        // remove unwanted properties
        for (var playerIndex in data.players) {
          delete data.players[playerIndex].index;
        }
        //send to server if data are ok
        if (self.warnings.length == 0) {
          console.log("sending data", data);
          var config = {
            method: "POST",
            url: "/api/v1/plays",
            headers: {
              "Content-Type": "application/javascript"
            },
            data: data
          };
          var req = $http(config).then(
            function(response) {
              // response is
              // { "msg":"a message", "data": play", "id":"play_id" }
              var added_play = JSON.parse(response.data.data);
              self.added_plays.push(added_play);
              self.initFields();
            },
            function(response) {
              self.warnings.push("Failed to POST new Play");
              console.log("failed to add new play", response);
            }
          );
        }
      }; //submitMyForm

      self.getGames();
      self.getPlayers();
      // depending on the action - init some fields@
      if (self.playId) {
        PlayResource.get({ playId: self.playId }).$promise.then(
          function(play) {
            if (self.action === "edit") {
              // nothing to do
            } else if (self.action === "rematch") {
              // remove id before initializing the fields
              delete play._id;
              delete self.playId;
            }
            self.initFields(play);
          },
          function(error) {
            var msg = "failed to find play with id " + self.playId;
            console.log(msg);
            self.warnings.push(msg);
          }
        );
      } else {
        self.initFields(null);
      }
    } //PlayNewController
  ]
}); // component
