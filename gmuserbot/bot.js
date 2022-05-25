const WebSocket = require('ws')
var faye = require('faye')
var request = require('request'); // library for GET/POST etc
const res = require('../local_variables.json') // bring in the local variables as a dict

var ws = new faye.Client("https://push.groupme.com/faye");
console.log('Starting bot!')

/*
	First, we need to use the GroupMe token to figure out the user_id of the 
	associated account. We use the `request` library for this
*/
request({
    url: "https://api.groupme.com/v3/users/me",
    qs: { "access_token": res.GROUPME_AUTH }
}, function(err, response, body) {
    if (err) {
        console.log(err);
        return;
    }
    console.log("Get response on USER_ID request: " + response.statusCode);
    MY_USER_ID = JSON.parse(response['body'])['response']['user_id'];


    /* 
    	Now that we have the user ID, we can set up the websockets with the proper
    	callback URL including that user ID.
    */
    ws.subscribe(`/user/${MY_USER_ID}`, (message) => {
        console.log(message.subject)
        if (message.type === 'ping') {
            return
        }
        forwardMessage(message.subject, res.token)
    }).then(() => {
        console.log("Ready!")
    })

    ws.addExtension({
        outgoing: function(message, callback) {
            if (message.channel !== '/meta/subscribe') return callback(message);
            message.ext = message.ext || {};
            message.ext.access_token = res.token;
            message.ext.timestamp = Math.floor(Date.now() / 1000)
            callback(message);
        }
    })
});

/* 
	Here's the meat of the work. This forwards the message on to the Python service
	to determine if responses need to be made. 
*/
function forwardMessage(message, token) {
    if (message) {
        if (message.text) {
        	request.post({
		  headers: {'content-type' : 'application/x-www-form-urlencoded'},
		  url:     res.forward_url,
		  body:    JSON.stringify(message)
		}, function(error, response, body){
		  console.log(body);
		});
            message.text = message.text.replace(/“|”/g, '"').replace(/‘|’/g, "'")
        }
    }
}