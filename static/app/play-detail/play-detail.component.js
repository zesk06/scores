"use strict";

// Register `playDetail` component, along with its associated controller and template
angular.module("playDetail").component("playDetailComponent", {
  bindings: { playId: "<" },
  templateUrl: "static/app/play-detail/play-detail.template.html",
  controller: [
    "PlayResource",
    "AuthCommon",
    "$http",
    "$state",
    function PhoneDetailController(PlayResource, AuthCommon, $http, $state) {
      var self = this;
      self.elos = [];
      self.auth = AuthCommon;
      PlayResource.get({ playId: self.playId }, function(play) {
        self.setPlay(play);
      });

      self.setPlay = function setPlay(play) {
        self.play = play;
        self.date = self.getDate(play.date);
        PlayResource.elos({ playId: self.playId }).$promise.then(function(
          elos
        ) {
          self.elos = elos;
        });
      };

      self.getDate = function getDate(timestamp) {
        //convert it to date using Date constructor
        return new Date(timestamp)
          .toISOString()
          .slice(0, 10)
          .replace(/-/g, "/");
      };

      self.getElo = function getElo(login) {
        for (var elo of self.elos) {
          if (elo.login === login) {
            return elo;
          }
        }
        return null;
      };

      self.deleteModal = function() {
        if (self.play) {
          // ask to confirm such an operation
          $("#myModal").modal();
        }
        return;
      };

      self.delete = function() {
        if (!self.play) {
          return;
        }
        //send DELETE request you fool
        console.log("DELETE ", self.play);
        self.delete_modal_play = undefined;
        var req = {
          method: "DELETE",
          url: "/api/v1/plays/" + self.playId
        };
        $http(req).then(
          function(response) {
            console.log("delete successfull", response);
            $("#myModal").on("hidden.bs.modal", function(e) {
              // redirect to index
              $state.go("index");
            });
            $("#myModal").modal("hide");
          },
          function(response) {
            console.log("delete failed", response);
            $("#myModal").modal("hide");
          }
        );
      };
    }
  ]
});
