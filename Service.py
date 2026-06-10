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
    schnitt = round(notensumme / len(student["belegungen"]), 2)

    if schnitt <= 2.5:
        return "grün"
    elif schnitt > 3:
        return "rot"
    else:
        return "gelb"

#fortscritt rechner
def frotscritt():

    #anteil an zeit seit anmeldung
    anmeldedatum = date.fromisoformat(student["anmeldedatum"])
    tagen_seit_anmeldung = (date.today() - anmeldedatum).days
    zeit_ziel = 365 * 3
    p_zeit = round((tagen_seit_anmeldung / zeit_ziel) * 100, 1)
    
    #anteil an erreichte ECTS
    gesamtects = 0
    for belegung in student["belegungen"]:
        ects = belegung["pruefung"]["modul"]["ects"]
        gesamtects += ects
    p_ects = round((gesamtects / studiengang["ects"]) * 100, 1)

    #unterschied zwischen % errechte ects und % abgelaufene zeit
    unterschied = p_ects - p_zeit
    if unterschied > 0:
        return "grün"
    elif unterschied < -5:
        return "rot"
    else:
        return "gelb"
    
#gesamtindikator
def gesamtindikator():
    note = notendurchnitt()
    zeit = frotscritt()
    if note == "rot" or zeit == "rot":
        return "rot"
    elif note == "gelb" or zeit == "gelb":
        return "gelb"
    else:
        return "grün"
    


