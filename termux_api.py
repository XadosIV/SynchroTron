import os
import json

def shell(cmd):
	#Appel une commande shell et renvoie son résultat
	return os.popen(cmd).read()

def choix_arret(arrets, title):
	cmd = 'termux-dialog radio -v "'
	valeurs = ""
	for i in arrets:
		valeurs+=i["name"]+","

	valeurs = valeurs[:-1] + '" '

	cmd += valeurs + '-t "' + title + '"'


	res = json.loads(shell(cmd))

	if res["code"] == -2:
		return "CLOSED"
	else:
		for i in arrets:
			if i["name"] == res["text"]:
				return i

		return "ERROR"

def choix_lignes(lignes, title):
	cmd = 'termux-dialog radio -v "'
	valeurs = ""
	for i in lignes:
		valeurs+="Ligne "+i["name"]+","

	valeurs = valeurs[:-1] + '" '

	cmd += valeurs + '-t "' + title + '"'


	res = json.loads(shell(cmd))

	if res["code"] == -2:
		return "CLOSED"
	else:
		for i in lignes:
			if i["name"] == res["text"]:
				return i

		return "ERROR"

def display(data):
	cmd = 'termux-dialog checkbox -v "'
	valeurs = ""
	for i in data:
		#data = {line, remaining, time, direction}
		valeurs+=f"[Ligne {i['line']}] Vers {i['direction']} à {i['time']} (Dans {i['remaining']})" + ","
	cmd += valeurs + '" -t "Résultats"'

	shell(cmd)

def spinner(choices, title):
	cmd = 'termux-dialog spinner -v "' + choices.join(',') + '" -t "' + title + '"'

	res = json.loads(shell(cmd))

	if res["code"] == -2:
		return "CLOSED"
	else:
		return res["text"]