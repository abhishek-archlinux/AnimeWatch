'use strict';
var args = require('system').args;
var isAuthenticating = false;
var page = require('webpage').create();
page.settings.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
page.settings.resourceTimeout = 30000
page.settings.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
page.settings.resourceTimeout = 30000
page.onResourceRequested = function(requestData, request) {
if ((/http:\/\/.+?\.css|http:\/\/.+?\.jpg|http:\/\/.+?\.gif|http:\/\/.+?\.png|http:\/\/.+?\.aspx|https:\/\/.+?\google|https:\/\/.+?\facebook|https:\/\/.+?\plugins/gi).test(requestData['url']) || requestData.headers['Content-Type'] == 'text/css|image/jpeg') {
//console.log('The url of the request is matching. Aborting: ' + requestData['url']);
request.abort();
}
};
page.open(args[1]);

page.onError = function () {
  return;
};

page.onInitialized = function () {
  page.evaluate(function () {
    window.navigator = {
      appName: 'Netscape',
      vendor: 'Google Inc.'
    };
  });
};

page.onLoadFinished = function(status) {
  if (isAuthenticating) {
    console.log(JSON.stringify(getCookies(), null, '  '));
    return setTimeout(phantom.exit, 0);
  }
  isAuthenticating = true;
};

/**
 * Retrieves interesting cookies.
 * @returns {!Array.<!Object>}
 */
function getCookies() {
  var cookies = [];
  Object.keys(phantom.cookies).forEach(function (key) {
    var cookie = phantom.cookies[key];
    if (!/.acb.im$/.test(cookie.domain)) return;
    cookies.push(cookie);
  });
  return cookies;
} 
