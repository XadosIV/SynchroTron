import requests as req
import json

url = "https://live.synchro-bus.fr/"
formatage = 'utf-8'


def get(endpoint):
	res = req.get(url+endpoint)
	return split(decode(res))


def decode(res):
	return res.content.decode(formatage)


def split(html):
	return html.split('<div class="nq-c-Content-directions">')[1].split("</section>")[0]


def raw_html_to_data(raw):
	return {
		"line": raw.split("_")[0][-1],
		"remaining": raw.split('dans ')[1].split("<")[0],
		"time": raw.split('detail-time">')[1].split("<")[0],
		"direction": raw.split("<span>")[1].split("</span>")[0]
	}


def horairesRapide(endpoint, direction):
	data = []

	if (direction != "-1"):
		endpoint += str(direction)
		endpoints = fix_endpoint([endpoint])

		endpoint = endpoints[0]

	html = get(endpoint)

	if (len(html.split("Aucun départ proche")) > 1):
		return "ERROR"

	dirs = html.split('<div class="nq-c-Direction-content">')

	for i in range(1, len(dirs)):
		data.append(raw_html_to_data(dirs[i]))

	return data


def horairesComplete(endpoint):
    endpoints = fix_endpoint([endpoint+"1", endpoint+"2"])

    data = []
    for endpoint in endpoints:
        data += horairesRapide(endpoint, "-1")

    return data


# Prend en compte toutes les bizarreries de synchrobus pour rendre les bons endpoint
def fix_endpoint(endpoints):
	res = []
	for endpoint in endpoints:
		if endpoint == "UJACO2":
			res.append("UJACO1")
		elif endpoint == "PLAG2":
			res.append("PLAG1")
		elif endpoint == "ROCNO2":
			res.append("ROCNO1")
		elif endpoint == "DEGAC2":
			res.append("DEGAC1")
		elif endpoint == "PRSON1" or endpoint == "PRSON2":
			res.append("PRSON")
		elif endpoint == "CHMNA2":
			res.append("CHMND2")
		elif endpoint == "CHMND1":
			res.append("CHMNA1")
		else:
			res.append(endpoint)

	if (len(res) > 1):
		if (res[0] == res[1]):
			return [res[0]]

	return res


def horaires(endpoint):
	with open("options.json", "r") as f:
		options = json.loads(f.read())

	if (options["fast-mode"]):
		return horairesRapide(endpoint, options["direction"])
	else:
		return horairesComplete(endpoint)


def readLinesJson():
	with open("lines.json", "r") as f:
		lines = json.loads(f.read())
	return lines


def getAllArrets(line=""):
	arrets = []

	lines = readLinesJson()

	for line_data in lines:
		if (line_data["code"] != line and line != ""):
			continue

		for arret in line_data["arrets"]:
			arrets.append(arret)

	return arrets


def getAllFavorites():
    arrets = []
    with open("favorites.json", "r") as f:
        fav = json.loads(f.read())

    allArrets = getAllArrets()
    for arret in allArrets:
        if arret["code"] in fav:
            arrets.append(arret)
            fav.remove(arret["code"])

    return arrets

def getAllNotFavorites():
	arrets = []
	with open("favorites.json", "r") as f:
		fav = json.loads(f.read())

	allArrets = getAllArrets()
	for arret in allArrets:
		if not (arret["code"] in fav):
			arrets.append(arret)

	return arrets

def getLines():
	lines_data = readLinesJson()
	lines = []
	for i in lines_data:
		lines.append(i["code"])
	return lines

"""
	TEST DES APPELS AUX ARRETS
for i in test:
	for j in i["arrets"]:
		code = j["code"]
		if len(code) <= 5 and code != "PRSON": #on exclut les cas sans chiffre à ajouter
			code += "2"


		res = horaires(code)

		if res != "ERROR":
			print(f"{code} OK")
		else:
			print(f"{code} ERROR")"""
