import json
import synchro_api as api
import termux_api as tapi


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
		else:
			return "ERROR"

spinner_options()