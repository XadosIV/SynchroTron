import json
import synchro_api as api
import termux_api as tapi
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

def load_options():
	with open("options.json", 'r') as f:
		options = json.loads(f.read())
	return options

def load_fav():
	with open("favorites.json", "r") as f:
		fav = json.loads(f.read())
	return fav

def save_fav(fav):
	with open("favorites.json", "w") as f:
		f.write(json.dumps(fav))

def add_favorite():
	arrets = api.getAllNotFavorites()
	arret = tapi.choix_arret(arrets, "Arrêt à ajouter aux favoris")
	if (arret == "CLOSED" or arret == "ERROR"):
		return
	fav = load_fav()
	fav.append(arret["code"])

	save_fav(fav)
	return True

def del_favorite():
	arrets = api.getAllFavorites()
	arret = tapi.choix_arret(arrets, "Arrêt à retirer des favoris")
	if (arret == "CLOSED" or arret == "ERROR"):
		return
	fav = load_fav()
	fav.remove(arret["code"])
	
	save_fav(fav)
	return True

def add_fast():
	fav = api.getAllFavorites()
	if (len(arrets) != 0):
    	arret = tapi.choix_arret(fav, "Créer un raccourci pour quel arrêt")
		if arret == "CLOSED":
			return
	directions = api.getDirection(arret)
	direction = tapi.radio(directions, "Quel direction ?")
	if direction == "CLOSED":
		return
	else:
		direction = direction["index"] + 1

	text = tapi.input_text("Entrer un nom", "Nom d'arrêt")
	if text == "CLOSED":
		return

	code = arret["code"] + direction
	
	infile = "python " + os.path.dirname(sys.argv[0]) + " " + code
	with open("~/.shortcuts/tasks/"+text.strip()+".sh", "w") as f:
		f.write(infile)


def del_fast():
	files = os.listdir("~/.shortcuts/tasks/")
	files.remove("Favoris.sh")
	files.remove("Options.sh")
	files.remove("Lines.sh")
	if len(files) == 0:
		return
	for f in len(files):
		files[f] = files[f].split(".")[0]

	name = tapi.radio(files, "Quel arret supprimer ?")
	name += ".sh"

	os.remove("~/.shortcuts/tasks/"+name)


def toggle_mode():
	options = load_options()
	options["fast-mode"] = not options["fast-mode"]
	with open("options.json", "w") as f:
		f.write(json.dumps(options))

def toggle_direction():
	options = load_options()
	options["direction"] = (options["direction"])%2+1
	with open("options.json", "w") as f:
		f.write(json.dumps(options))


def spinner_options():
	choices = []

	if (len(api.getAllNotFavorites()) != 0):
		choices.append("Ajouter un favori")

	if (len(api.getAllFavorites()) != 0):
		choices.append("Retirer un favori")

	options = load_options()
	if options["fast-mode"]:
		choices.append("[Mode Rapide] Passer en mode Complet")
	else:
		choices.append("[Mode Complet] Passer en mode Rapide")

	if options["direction"] == 1:
		choices.append("Definir direction: Jacob/Maison Brulee/De Gaulle")
	else:
		choices.append("Definir direction: Technolac/Roc Noir/Challes Centre")

	choices.append("Creer un arret rapide")
	if len(os.listdir("~/.shortcuts/tasks/")) > 3:
		choices.append("Supprimer un arret rapide")

	choice = tapi.spinner(choices, "Options")

	if (choice == "CLOSED"):
		return
	else:
		if choice == "Ajouter un favori":
			add_favorite()
		elif choice == "Retirer un favori":
			del_favorite()
		elif choice.startswith("[Mode"):
			toggle_mode()
		elif choice.startswith("Definir"):
			toggle_direction()
		elif choice == "Creer un arret rapide":
			add_fast()
		elif choice == "Supprimer un arret rapide":
			del_fast()
		else:
			return "ERROR"

spinner_options()
