'use strict';

// Register `playDetail` component, along with its associated controller and template
angular.
    module('playDetail').
    component('playDetailComponent', {
        bindings: { playId: '<' },
        templateUrl: 'static/app/play-detail/play-detail.template.html',
        controller: ['PlayResource',
            function PhoneDetailController(PlayResource) {
                var self = this;

                self.elos = [];

                PlayResource.get({ playId: self.playId }, function (play) {
                    self.setPlay(play);
                });

                self.setPlay = function setPlay(play) {
                    self.play = play;
                    self.date = self.getDate(play.date);
                    PlayResource.elos({ playId: self.playId }).$promise.then(function(elos) {
                        self.elos = elos;
                    });
                };

                self.getDate = function getDate(timestamp) {
                    //convert it to date using Date constructor
                    return new Date(timestamp).toISOString().slice(0, 10).replace(/-/g, "/");
                };

                self.getElo = function getElo(login){
                    for(var elo of self.elos){
                        if(elo.login === login){
                            return elo;
                        }
                    }
                    return null;
                }
            }
        ]
    });
