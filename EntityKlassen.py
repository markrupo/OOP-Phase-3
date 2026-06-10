from datetime import date
from enum import Enum

class Student:
    def __init__(self, name, anmeldedatum):
        self.name = name
        self.anmeldedatum = anmeldedatum
        self.belegungen = []
 
class Pruefung:
    def __init__(self, pruefungstyp, modul):
        self.pruefungstyp = pruefungstyp
        self.modul = modul

class Modul:
    def __init__(self, name, ects):
        self.name = name
        self.ects = ects

class Studiengang:
    def __init__(self, name, ects):
        self.name = name
        self.ects = ects
        self.module = []        

class Pruefungstyp(Enum):
    Klausur = "Klausur"
    Workbook = "Workbook"
    Portfolio = "Portfolio"
    Präsentation = "Präsentation"

class Belegung:
    def __init__(self, note, pruefung, pruefungsdatum):
        self.note = note
        self.pruefung = pruefung
        self.pruefungsdatum = pruefungsdatum

    def bestanden(self):
        if self.note <= 4.0:
            return True
        else:
            return False