import termux_api as tapi
import synchro_api as api

line = tapi.choix_lignes(api.getLines(), "Choix de la ligne")
arrets = api.getAllArrets(line)

if (len(arrets) != 0):

    arret = tapi.choix_arret(arrets, "Arrets ligne "+line)
    data = api.horaires(arret["code"])
    tapi.display(data)
