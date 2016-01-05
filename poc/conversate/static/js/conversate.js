angular.module('conversateApp', ['ngRoute', 'emguo.poller'])

.directive('onLastRepeat', function() {
  // custom directive to give an on render handler to scroll to bottom of viewpane
  return function(scope, element, attrs) {
    if (scope.$last) setTimeout(function(){
      scope.$emit('onRepeatLast', element, attrs);
    }, 1);
  };
})

.config(
  function($routeProvider, $locationProvider) {
    $routeProvider.when('/conversate/:partner', {
      templateUrl: '/static/partials/messages.html',
      controller: 'AllMessagesController'
    });
    $locationProvider.html5Mode({ enabled: true, requireBase: false });
  }
)

.controller('SubmitMessageController', function ($scope, $http) {
  $scope.submit = function(partnerUsername) {
    $http.post("/conversate/send_message/" + partnerUsername + "/", { message: $scope.message })
      .success(function (data, status, headers, config) {
        console.log('sent message success, status: ' + status);
      })
      .error(function (data, status, headers, config) {
        console.log('sent message success, error: ' + status);
      });
    $scope.message = "";
    $scope.form.$setPristine(true);
    $scope.form.$setUntouched();
  };
})

.controller('AllMessagesController', function ($scope, $http, $routeParams, poller) {
  $scope.recipient = $routeParams.partner;
  $http.get('/conversate/api/' + $routeParams.partner).success(function(data) {
    // getting first page in reverse ordering, show most recent at the tail
    $scope.messages = data.results.reverse();

    var getLastId = function() {
      if ($scope.messages.length > 0) {
        return $scope.messages[$scope.messages.length - 1].id;
      } else {
         return 0;
      }
    };
    var newMessagePoller = poller.get('/conversate/api/' + $routeParams.partner + '/since/', {
      action: 'get',
      delay: 2000,
      argumentsArray: [
        {
          params: {
            "last_id" : getLastId()
          }
        }
      ]
    });
    $scope.poller = newMessagePoller;
    newMessagePoller.promise.then(null, null, function(response) {
      $scope.messages.push.apply($scope.messages, response.data.results);
      // updatet poller last_id arg
      $scope.poller.argumentsArray[0].params['last_id'] = getLastId();
    });

  });

  // scroll to end of message window to display the most recent 
  $scope.$on('onRepeatLast', function(scope, element, attrs){
    $("#msgcontainer").scrollTop($("#msgcontainer")[0].scrollHeight);
  });

});