from DatenManager import *
from EntityKlassen import *
from datetime import date



class Service:

    def __init__(self):
        self.student, self.studiengang = laden()

    # Noten durchscnitt berechner
    def notendurchschnitt(self):

        geschaffte_pruefungen = 0
        notensumme = 0
        for belegung in self.student.belegungen:
            if belegung.note >= 4:
                notensumme += belegung
                geschaffte_pruefungen += 1
        
        if self.student.belegungen:
            schnitt = round(notensumme / len(self.student.belegungen), 2)
        else:
            return "keine belegungen"

        if schnitt <= 2.5:
            return "grün", None
        elif schnitt > 3:
            return "rot", "Note deutlich unter ziel"
        else:
            return "gelb", "Note unter ziel"

    #fortscritt rechner
    def fortschritt(self):
        
        #anteil an zeit seit anmeldung
        anmeldedatum = self.student.anmeldedatum.date()
        tagen_seit_anmeldung = (date.today() - anmeldedatum).days
        zeit_ziel = 365 * 3
        p_zeit = round((tagen_seit_anmeldung / zeit_ziel) * 100, 1)
        
        #anteil an erreichte ECTS
        gesamtects = 0
        for belegung in self.student.belegungen:
            if belegung.note >= 4:
                ects = belegung.pruefung.modul.ects
                gesamtects += ects
        p_ects = round((gesamtects / self.studiengang.ects) * 100, 1)

        #unterschied zwischen % errechte ects und % abgelaufene zeit
        unterschied = p_ects - p_zeit
        if unterschied > 0:
            return "grün", None
        elif unterschied < -5:
            return "rot", "Tempo deutlich unter ziel"
        else:
            return "gelb", "Tempo unter ziel"
        
    #gesamtindikator
    def gesamtindikator(self):
        note = self.notendurchschnitt()
        zeit = self.fortschritt()

        erklaerung = [note[1], zeit[1]]
        if erklaerung[1] == None:
            erklaerung.remove(None)
        
        if erklaerung[0] == None:
            erklaerung.remove(None)

        if note[0] == "rot" or zeit[0] == "rot":
            return ["rot"] + erklaerung
        elif note[0] == "gelb" or zeit[0] == "gelb":
            return ["gelb"] + erklaerung
        else:
            return "grün"
                
    def belegungen(self):
        print(f"Insgesamt {len(self.student.belegungen)} belegungen")
        for i, belegung in enumerate(self.student.belegungen, start=1):
            print("-" * 20)
            print(i)
            print(f"Modul: {belegung.pruefung.modul.name}")
            print(f"Note: {belegung.note}")
            print(f"Art der Prüfung: {belegung.pruefung.pruefungstyp.value}")
            print(f"Datum: {belegung.pruefungsdatum.date()}")
            print("-" * 20)
            
    def pruefung_belegen(self, modul, note_eingabe, pruefungstyp_eingabe):
        if modul < 1 or modul > len(self.studiengang.module):
            return "falsches index"
        modul -= 1
        for belegung in self.student.belegungen:
            if belegung.pruefung.modul == self.studiengang.module[modul] and belegung.note <= 4:
                return f"Prüfung im fach {belegung.pruefung.modul.name} bereits bestanden"
        
        m = self.studiengang.module[modul]
        p = Pruefung(pruefungstyp_eingabe, m)
        neue_belegung = Belegung(note_eingabe, p, date.today())
        belegungen = self.student.belegungen
        belegungen.append(neue_belegung)
        speichern(self.student, self.studiengang)
        print(f"prüfung belegt")

    def modul_liste(self):
        for i, modul in enumerate(self.studiengang.module, start=1):
            print(f"{i}. {modul.name:<25} ECTS: {modul.ects}")
    

