import termux_api as tapi
import synchro_api as api

line = tapi.choix_lignes(api.getLines(), "Choix de la ligne")
codeLine = line.split(" ")[1]
arrets = api.getAllArrets(codeLine)

if (len(arrets) != 0):

	arret = tapi.choix_arret(arrets, "Arrets Favoris")
	data = api.horaires(arret["code"])
	tapi.display(data)