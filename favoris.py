import termux_api as tapi
import synchro_api as api

arrets = api.getAllFavorites()

if (len(arrets) != 0):

	arret = choix_arret(arrets, "Arrets Favoris")
	data = api.horaires(arret)
	tapi.display(data)