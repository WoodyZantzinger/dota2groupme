import os
import urllib2
import urllib
import traceback
from flask import Flask, request
from dota2py import api
from dota2py import data


GroupMetoSteam = {
      'Woody Zantzinger' : 'Azohko',
      'Andy Esposito' : 'Espo',
      'Sty' : 'Wink91'
}

GroupMetoDOTA = {
	'Woody Zantzinger' : 30075956,
	'Andy Esposito' : 84388592,
	'Sty' : 78479931
}

key =  "63760574A669369C2117EA4A30A4768B"


help_dict = {"#last" : "Shows your personel stats from the last game, add a user argument to find someone elses stats",
           "#now" : "Shows who is currently online (NOT IMPLEMENTE YET)",
           "#setSteam" : "Set your SteamID if not hardcoded in yet. This is you Steam (Not Dota) username.",
           "#setDOTA" : "This is your Dota ID number. Find this as the last number in your DotaBuff URL",
           "#status" : "See if sUN bot is up",
           "#help" : "You are reading the help now..."
}

app = Flask(__name__)
#
# https://api.groupme.com/v3/bots/post

def send_message(msg):
	print "Sending " + msg
	url = 'https://api.groupme.com/v3/bots/post'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	header = { 'User-Agent' : user_agent }
	values = {
      'bot_id' : '535cbd947cf38b46a83fa3084f',
      'text' : msg,
	}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, header)
	response = urllib2.urlopen(req)
	#print "msg"
	return response
	#return 'Win'
	
def set_steam(msg, user):
	print "Got here"
	GroupMetoSteam[user] = msg
	return send_message("I set your Steam ID to: " + msg )
	
def set_dota(msg, user):
	print "Got here"
	GroupMetoDOTA[user] = msg
	return send_message("I set your Dota ID to: " + msg )
	

def last_game(msg, user):
	
	print "Starting"
	
	if not GroupMetoSteam.has_key(user):
		send_message("I don't know your SteamID! Set it with '#set ID'")
		return 'OK'
		
	if not GroupMetoDOTA.has_key(user):
		send_message("I don't know your DOTA ID! Set it with '#setDota ID'")
		return 'OK'
		
	print "Setting Key"	
	api.set_api_key(key)
	
	print "Getting Data"	
	# Get all the most recent match played by the player
	account_id = int(api.get_steam_id(GroupMetoSteam[user])["response"]["steamid"])
	print "Got Account ID"
	# Get a list of recent matches for the player
	matches = api.get_match_history(account_id=account_id)["result"]["matches"]

	#Get the full details for a match
	match = api.get_match_details(matches[0]["match_id"])
	print "Got Match Details"
	for x in match["result"]["players"]:
		if int(x["account_id"]) == GroupMetoDOTA[user]:
			print "Got User Data"
			send_message ("As " + data.get_hero_name(x["hero_id"])["localized_name"] + " you went " + str(x["kills"]) + ":" + str(x["deaths"]) + ":" + str(x["assists"]) + " with " + str(x["gold_per_min"]) + " GPM")
	return 'OK'

def current_online(msg, user):
	return send_message("No one is online!")

def help(msg, user):
	send_message("Fuck you " + str(user) + "... This shit isn't that hard")
	for command, help_text in help_dict.iteritems():
		send_message(command + ": " + help_text)
	return 'OK'

def status(msg, user):
	return send_message("Currently listening...")


options = {"#last" : last_game,
           "#now" : current_online,
           "#setSteam" : set_steam,
           "#setDOTA" : set_dota,
           "#status" : status,
           "#help" : help,
}



@app.route('/message/', methods=['POST'])
def message():
	new_message = request.get_json(force=True)
	sender = new_message["name"]
	body = new_message["text"]
	if body.startswith("#"):
		print "Calling: " + body.partition(' ')[0] + " With " + body.partition(' ')[2]
		
		try:
			options[body.partition(' ')[0]](body.partition(' ')[2], sender)
		except BaseException as e:
			print repr(e)
    		traceback.print_exc()
	return 'OK'

@app.route("/")
def hello():
	return "Hello world!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(host='0.0.0.0', port=port, debug=True)