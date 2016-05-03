'use strict';

describe('Service: ardyhServices.js', function () {

  // load the service's module
  beforeEach(module('webappApp'));

  // instantiate service
  var ardyhServices.js;
  beforeEach(inject(function (_ardyhServices.js_) {
    ardyhServices.js = _ardyhServices.js_;
  }));

  it('should do something', function () {
    expect(!!ardyhServices.js).toBe(true);
  });

});
