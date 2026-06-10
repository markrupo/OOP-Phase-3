from DatenManager import *
from datetime import date, timedelta

daten = laden()
student = daten["student"]
studiengang = daten["studiengang"]

# Noten durchscnitt berechner
def notendurchnitt():
    notensumme = 0
    for belegung in student["belegungen"]:
        notensumme += belegung["note"]
    schnitt = notensumme / len(student["belegungen"])
    return round(schnitt, 2)




def frotscritt():
    anmeldedatum = date.fromisoformat(student["anmeldedatum"])
    tagen_seit_anmeldung = (date.today() - anmeldedatum).days
    zeit_ziel = days=365 * 3
    prozentanteil = round((tagen_seit_anmeldung / zeit_ziel) * 100, 1)
    gesamtects = 0
    for belegung in student["belegungen"]:
        belegung




