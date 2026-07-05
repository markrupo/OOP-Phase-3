from DatenManager import *
from EntityKlassen import *
from datetime import date



class Service:

    def __init__(self):
        self.student, self.studiengang = laden()

    def notendurchschnitt(self):
        """Teilt die Note aller bestandenen Belegungen durch die Anzahl der bestandenen Belegungen"""
        geschaffte_pruefungen = 0
        notensumme = 0
        for belegung in self.student.belegungen:
            if belegung.note <= 4:
                notensumme += belegung.note
                geschaffte_pruefungen += 1
        
        if self.student.belegungen:
            return round(notensumme / geschaffte_pruefungen, 2)
        else:
            return "keine belegungen"
        
    def notenschnitt_status(self):
        """Vergleicht den Schnitt mit dem Zielschnitt und gibt einen Kreis in der entsprechenden Farbe aus"""
        schnitt = self.notendurchschnitt()
        if isinstance(schnitt, str):
            return schnitt
        elif schnitt <= self.student.noten_ziel:
            return "\U0001F7E2", None
        elif schnitt > self.student.noten_ziel +0.5:
            return "\U0001F534", "Note deutlich unter ziel"
        else:
            return "\U0001F7E1", "Note unter ziel"
    
    def anteil_zeit_seit_anmeldung(self):
        """Rechnet wie viel Zeit bis zum Ziel bereits abgelaufen ist"""
        anmeldedatum = self.student.anmeldedatum
        tagen_seit_anmeldung = (date.today() - anmeldedatum).days
        zeit_ziel = self.student.zeit_ziel * 365
        p_zeit = round((tagen_seit_anmeldung / zeit_ziel) * 100, 1)
        return p_zeit
    
    def anteil_zeit_zeiger(self):
        """Zeigt grafisch wie viel Zeit bis zum Ziel bereits abgelaufen ist"""
        p_zeit = self.anteil_zeit_seit_anmeldung()
        anzahl_volle_vierecke = round((p_zeit / 100) * 36)
        anzahl_lehre_vierecke = 36 - anzahl_volle_vierecke
        zeiger = anzahl_volle_vierecke * "■" + anzahl_lehre_vierecke * "□"
        return zeiger

    def erreichte_ects(self):
        """Rechnet wie viele ECTS geschafft wurden"""
        gesamtects = 0
        for belegung in self.student.belegungen:
            if belegung.note <= 4:
                ects = belegung.pruefung.modul.ects
                gesamtects += ects
        return gesamtects

    def anteil_erreichte_ects(self):
        """Rechnet den Anteil an erreichten ECTS aus"""
        p_ects = round((self.erreichte_ects() / self.studiengang.ects) * 100, 1)
        return p_ects
    
    def anteil_ects_zeiger(self):
        """Zeigt grafisch den Anteil der erreichten ECTS"""

        p_ects = self.anteil_erreichte_ects()
        anzahl_volle_vierecke = round((p_ects / 100) * 36)
        anzahl_lehre_vierecke = 36 - anzahl_volle_vierecke
        zeiger = anzahl_volle_vierecke * "■" + anzahl_lehre_vierecke * "□"
        return zeiger

    def fortschritt(self):
        """Rechnet die Differenz zwischen dem Anteil der erreichten ECTS und dem Anteil der Zeit seit der Anmeldung und gibt einen Kreis in der entsprechenden Farbe aus"""
        unterschied = self.anteil_erreichte_ects() - self.anteil_zeit_seit_anmeldung()
        if unterschied > 0:
            return "\U0001F7E2", None
        elif unterschied < -5:
            return "\U0001F534", "Tempo deutlich unter ziel"
        else:
            return "\U0001F7E1", "Tempo unter ziel"
        
    def gesamtindikator(self):
        """Zeigt rot wenn mindestens eines der anderen Ziele bei Rot liegt, gelb, wenn mindestens ein Ziel bei Gelb liegt aber keins bei Rot, und grün, wenn beide Ziele im grünen Bereich liegen"""
        note = self.notenschnitt_status()
        zeit = self.fortschritt()

        erklaerung = [note[1], zeit[1]]

        if note[0] == "\U0001F534" or zeit[0] == "\U0001F534":
            return ["\U0001F534"] + erklaerung
        elif note[0] == "\U0001F7E1" or zeit[0] == "\U0001F7E1":
            return ["\U0001F7E1"] + erklaerung
        else:
            return "\U0001F7E2" + erklaerung
    
    def noten_ziel_aendern(self, ziel):
        """Ändert das Notenziel"""
        try:
            float(ziel)
        except ValueError:
            return "Das Notenziel muss eine Zahl sein"
        
        if float(ziel) > 4 or float(ziel) < 1:
            return "Das Ziel darf nicht kleiner als 1 oder großer als 4 sein"
        else:
            self.student.noten_ziel = float(ziel)
            speichern(self.student, self.studiengang)
            return "Notenziel verändert"
    
    def zeit_ziel_aendern(self, ziel):
        """Ändert das Zeitziel"""
        try:
            float(ziel)
        except ValueError:
            return "Das Zeitziel muss eine Zahl sein"
        ziel = float(ziel)
        if ziel > 6:
            return "Die maximale Studiendauer beträgt 6 Jahren, bitte geben Sie einen niedrigeren Wert ein"
        else:
            self.student.zeit_ziel = float(ziel)
            speichern(self.student, self.studiengang)
            return "Zeit ziel geändert"
        
    def pruefung_belegen(self, modul, note_eingabe, pruefungstyp_eingabe):
        """Stellt ein Belegung Objekt mit den eingegebenen Daten her"""
        try:
            int(modul)
        except ValueError:
            return "Falsches modul index"
        try:
            float(note_eingabe)
        except ValueError:
            return "Die note muss eine Zahl sein"
        try:
            int(pruefungstyp_eingabe)
        except ValueError:
            return "Ungültigen prüfungstyp"
        
        if pruefungstyp_eingabe == "1":
            pruefungstyp_eingabe = "Klausur"
        elif pruefungstyp_eingabe == "2":
            pruefungstyp_eingabe = "Workbook"
        elif pruefungstyp_eingabe == "3":
            pruefungstyp_eingabe = "Portfolio"
        elif pruefungstyp_eingabe == "4":
            pruefungstyp_eingabe = "Präsentation"
        else:
            return "ungültige Eingabe"
        modul = int(modul)
        if modul < 1 or modul > len(self.studiengang.module):
            return "falsches modul index"
        modul -= 1
        note_eingabe = float(note_eingabe)
        if note_eingabe > 6:
            return "Die maximale note beträgt 6"
        
        for belegung in self.student.belegungen:
            if belegung.pruefung.modul == self.studiengang.module[modul] and belegung.note <= 4:
                return f"Prüfung im fach {belegung.pruefung.modul.name} bereits bestanden"
        
        m = self.studiengang.module[modul]
        p = Pruefung(Pruefungstyp(pruefungstyp_eingabe), m)
        neue_belegung = Belegung(note_eingabe, p, date.today())
        self.student.belegungen.append(neue_belegung)
        speichern(self.student, self.studiengang)
        return "prüfung belegt"

    def modul_liste(self):
        """Fügt alle Module mit ihren Infos in eine Liste und unterscheidet zwischen belegt und nicht belegt"""
        liste = []

        for i, modul in enumerate(self.studiengang.module, start=1):
            belegt = 0
            note = 0
            for belegung in self.student.belegungen:
                if belegung.note <= 4 and belegung.pruefung.modul == modul:                        
                    belegt += 1
                    note += belegung.note
                    break
            if belegt == 0:
                liste.append(f"{i:<3} {modul.name:<68} | ECTS: {modul.ects:<2} | --- | Offen")
            else:
                liste.append(f"{i:<3} {modul.name:<68} | ECTS: {modul.ects:<2} | { float(note)} | Belegt")                
        return liste

