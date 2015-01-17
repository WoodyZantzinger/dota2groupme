
GroupMetoSteam = {
      'Woody Zantzinger' : 76561197990341684,
      'Andy Esposito' : 76561198044654320,
      'Sty' : 76561198038745659,
      'Armadilldo' : 76561198067289145,
      'Matthew' : 76561198079784406,
      'Kevin' : 76561198097020021,
      'Jonny G' : 76561198025357651,
}

GroupMetoDOTA = {
	'Woody Zantzinger' : 30075956,
	'Andy Esposito' : 84388592,
	'Sty' : 78479931,
	'Armadilldo' : 107023417,
	'Matthew' : 119518678,
	'Kevin' : 136754293,
	'Jonny G' : 65091923,
}

def name_to_dotaID(name):
	return int(GroupMetoDOTA[name])

def has_dotaID(name):
	return GroupMetoDOTA.has_key(name)
	
def has_steamID(name):
	return GroupMetoSteam.has_key(name)
	
def name_to_steamID(name):
	return int(GroupMetoSteam[name])
	