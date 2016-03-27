var page = require('webpage').create();
var args = require('system').args;
var url = args[1];
page.settings.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'

page.settings.resourceTimeout = 30000
page.onResourceRequested = function(requestData, request) {
if ((/http:\/\/.+?\.css|http:\/\/.+?\.jpg|http:\/\/.+?\.gif|http:\/\/.+?\.png|http:\/\/.+?\.aspx|https:\/\/.+?\google|https:\/\/.+?\facebook|https:\/\/.+?\plugins/gi).test(requestData['url']) || requestData.headers['Content-Type'] == 'text/css|image/jpeg') {
//console.log('The url of the request is matching. Aborting: ' + requestData['url']);
request.abort();
}
};


page.open(url, function(status) {
 if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit();
    } else {
	window.setTimeout(function () {
 		var v = page.evaluate(function() {
   		return document.documentElement.innerHTML;
 		});
 		//console.log(JSON.stringify(v));
 		console.log(v)
		 phantom.exit();
},10000)}});




