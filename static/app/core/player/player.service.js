"use strict";

angular.module("core.player").factory("PlayerResource", [
  "$resource",
  // see $resource documentation:
  // https://docs.angularjs.org/api/ngResource/service/$resource
  function($resource) {
    return $resource("api/v1/players/:playerId");
  }
]);
