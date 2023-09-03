import termux_api as tapi
import synchro_api as api

arrets = api.getAllFavorites()
if (len(arrets) != 0):
    arret = tapi.choix_arret(arrets, "Arrets Favoris")
    if arret != "CLOSED":
        data = api.horaires(arret["code"])
        tapi.display(data)
