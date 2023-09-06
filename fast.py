import synchro_api as api
import termux_api as tapi
import sys

if len(sys.argv) == 1:
	exit()
else:
	data = api.horaires(sys.argv[1])
	tapi.display(data)