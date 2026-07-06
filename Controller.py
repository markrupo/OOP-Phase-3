from Service import Service
from KommandoDarstellung import View
import os


class controller:
    def __init__(self):
        self.service = Service()
        self.view = View()
    
    def dashboard_zeigen(self):
        """Gibt Daten vom Service an die View weiter um das Dashboard zu erstellen"""
        self.view.banner(
            self.service.gesamtindikator(),
            self.service.student.name,
            self.service.studiengang.name
            )
        
        self.view.zeit(
            self.service.fortschritt()[0],
            self.service.erreichte_ects(),
            self.service.studiengang.ects,
            self.service.anteil_ects_zeiger(),
            self.service.anteil_zeit_seit_anmeldung(),
            self.service.anteil_erreichte_ects(),
            self.service.anteil_zeit_zeiger()
        )
        
        self.view.note(
            self.service.notenschnitt_status()[0],
            self.service.notendurchschnitt(),
            self.service.student.noten_ziel,
            self.service.notenschnitt_status()[1]
        )


    def nutzer_eingabe(self):
        """Erlaubt Nutzern die Interaktion mit dem Programm"""
        eingabe = input(f"{"\n" * 2}1 = Dashboard\n2 = Belegungen\n3 = Module zeigen\n4 = Modul belegen\n5 = Notenziel ändern\n6 = Zeitziel ändern\nzahl eingeben:")
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if eingabe == "1":
            self.dashboard_zeigen()

        elif eingabe == "2":
            """Gibt Daten vom Service an View weiter um bestandene Belegungen anzuzeigen"""
            self.view.belegungen(len(self.service.student.belegungen),self.service.student.belegungen)

        elif eingabe == "3":
            """Gibt Daten vom Service an View weiter um alle Module zu zeigen"""
            self.view.print_alle_module(self.service.modul_liste())

        elif eingabe == "4":
            """Nimmt die Nutzereingabe entgegen und erstellt ein Belegung Objekt"""
            modul_index = input("0 = Zurück zum Dashboard\nModul index aus der modul liste eingeben:")
            if modul_index == "0":
                return self.dashboard_zeigen()
            os.system('cls' if os.name == 'nt' else 'clear')
            note = input("0 = Zurück zum Dashboard\nNote eingeben:")
            if note == "0":
                return self.dashboard_zeigen()
            os.system('cls' if os.name == 'nt' else 'clear')
            pruefungstyp = input("0 = Zurück zum Dashboard\n1 = Klausur\n2 = Workbook\n3 = Portfolio\n4 = Präsentation\nZahl eingeben:")
            if pruefungstyp == "0":
                return self.dashboard_zeigen()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.service.pruefung_belegen(modul_index, note, pruefungstyp))

        elif eingabe == "5":
            """Nimmt die Nutzereingabe entgegen und ändert das Notenziel"""
            eingabe = input("0 = Zurück zum Dashboard\nneues ziel setzen:")
            if eingabe == "0":
                return self.dashboard_zeigen()
            else:
                print(self.service.noten_ziel_aendern(eingabe))

        elif eingabe == "6":
            """Nimmt die Nutzereingabe entgegen und ändert das Zeitziel"""
            eingabe = input("0 = Zurück zum Dashboard\nneues ziel setzen:")
            if eingabe == "0":
                return self.dashboard_zeigen()
            else:
                print(self.service.zeit_ziel_aendern(eingabe))

    def run(self):
        """Startet das Programm"""
        while True:
            self.nutzer_eingabe()
            

c = controller()
c.run()
