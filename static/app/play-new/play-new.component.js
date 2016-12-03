'use strict';

angular.
    module('playNew').
    component('playNewComponent', {
        bindings: { playId: '<' },
        templateUrl: 'static/app/play-new/play-new.template.html',
        controller: ['PlayResource', 'GameResource', 'PlayerResource', '$http',
            function PlayNewController(PlayResource, GameResource, PlayerResource, $http) {
                var self = this;
                // An object to retrieve the form values
                self.date_s = new Date();
                self.time_s = new Date();
                self.time_s.setSeconds(0);
                self.time_s.setMilliseconds(0);
                self.infos = [];
                self.warnings = [];

                // The new player default values
                self.new_player = {
                    login: "",
                    score: 0,
                    color: "",
                    role: "",
                    team: "",
                    team_color: ""
                }
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
                self.initFields = function(){
                    self.fields = {
                        game: "",
                        date: 0,
                        wintype: "max",
                        comment: "",
                        players: [],
                        winners: [],
                        winners_reason: []
                    }
                }
                self.addPlayer = function (login) {
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
                }

                self.removePlayer = function (player) {
                    for (var index in self.fields.players) {
                        if (self.fields.players[index].index === player.index) {
                            self.fields.players.splice(index, 1);
                        }
                    }
                }

                self.setGame = function (game) {
                    self.fields.game = game;
                }

                self.getGames = function(){
                    self.games = GameResource.query();
                }

                self.getPlayers = function(){
                    self.players = PlayerResource.query();
                }

                self.submitMyForm = function () {
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
                        console.log('sending data', data);
                        var config = {
                            method: 'POST',
                            url: '/api/v1/plays',
                            headers: {
                                'Content-Type': 'application/javascript'
                            },
                            data: data
                        };
                        var req = $http(config).then(function (response) {
                            self.infos.push('Added new play ' + response.data.id);
                            self.initFields();
                        }, function (response) {
                            self.warnings.push('Failed to POST new Play');
                            console.log('failed to add new play', response);
                        });
                    };
                }//submitMyForm
                self.initFields();
                self.getGames();
                self.getPlayers();
            }//PlayNewController
        ]
    });// component
