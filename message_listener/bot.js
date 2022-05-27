const WebSocket = require('ws')
var faye = require('faye')
var ws = new faye.Client("https://push.groupme.com/faye");
const res = require('../local_variables.json')
const url = require('node:url');
const https = require('https')
const axios = require('axios')

// get user_id from token
const requestUrl = url.parse(url.format({
    protocol: 'https',
    hostname: 'api.groupme.com',
    pathname: '/v3/users/me',
    query: {
        access_token: res.GROUPME_AUTH
    }
}));

let request_call = new Promise((resolve, reject) => {
    https.get({
        hostname: requestUrl.hostname,
        path: requestUrl.path,
    }, (response) => {
        let chunks_of_data = [];

        response.on('data', (fragments) => {
            chunks_of_data.push(fragments);
        });

        response.on('end', () => {
            let response_body = Buffer.concat(chunks_of_data);

            // promise resolved on success
            resolve(response_body.toString());
        });

        response.on('error', (error) => {
            // promise rejected on error
            reject(error);
        });
    });
});

request_call.then((response) => {
    user_id = JSON.parse(response).response.id;
    ws.subscribe(`/user/${user_id}`, (message) => {
        console.log(message.subject)
        if (message.type === 'ping') {
            return
        }
        //checkMessages(message.subject, res.token)
        doPost(message.subject);
    }).then(() => {
        console.log("Ready!")
    })

    ws.addExtension({
        outgoing: function(message, callback) {
            if (message.channel !== '/meta/subscribe') return callback(message);
            message.ext = message.ext || {};
            message.ext.access_token = res.GROUPME_AUTH;
            message.ext.timestamp = Math.floor(Date.now() / 1000)
            callback(message);
        }
    })
}).catch((error) => {
    console.log(error);
});


function doPost(message) {

    axios.post("https://young-fortress-3393.herokuapp.com/message/?type=Message", JSON.stringify(message))
    .then((response) => {
      // console.log(response);
    }, (error) => {
      // console.log(error);
    });

}