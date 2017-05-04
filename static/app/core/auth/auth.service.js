"use strict";

angular.module("core.auth").factory("AuthCommon", function() {
  return {
    getLoggedUser: function() {
      return document.user_is_logged;
    },
    isLogged: function() {
      return document.user_is_logged !== undefined;
    }
  };
});
