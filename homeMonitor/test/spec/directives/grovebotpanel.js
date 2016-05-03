'use strict';

describe('Directive: grovebotPanel', function () {

  // load the directive's module
  beforeEach(module('homeMonitor'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<grovebot-panel></grovebot-panel>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the grovebotPanel directive');
  }));
});
