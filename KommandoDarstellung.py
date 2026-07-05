from Service import *
from DatenManager import *

class View:  

    def banner(self, gesamtindikator, student_name, studiengang_name):
        """Druckt die Infos aus dem Gesamtindikator"""    
        print("=" * 50 + "\n")
        print(f"{"Gesamtindikator:":>32} {gesamtindikator[0]}")
        if gesamtindikator[1]: print(f"{gesamtindikator[1]:^52}""\n")
        if gesamtindikator[2]: print(f"{gesamtindikator[2]:^52}""\n")
        print("=" * 50 + "\n")

        print(f"Student: {student_name}")
        print(f"Studiengang: {studiengang_name}\n")
    
    def zeit(self,
             farbe_ball,
             erreichte_ects,
             studiengang_ects,
             anteil_ects_zeiger, 
             anteil_zeit_seit_anmeldung,
             anteil_erreichte_ects,
             anteil_zeit_zeiger):
        """Druckt relevante Infos zur Studienzeit"""
        
        print(f"{"Studienzeit:":>19} {farbe_ball}""\n")
        print(f"{"Erreichte ECTS:":>22} {erreichte_ects}/{studiengang_ects} = {anteil_erreichte_ects}%")
        print(f"{anteil_ects_zeiger:^50}""\n")
        print(f"{"Zeit bis Ziel":>20} {anteil_zeit_seit_anmeldung}%")
        print(f"{anteil_zeit_zeiger:^50}""\n""\n")

    def note(self, 
             farbe_ball,
             notendurchschnitt,
             noten_ziel,
             erklärung):
        """Druckt relevante Infos über Noten"""
        print(f"\n{"Notenschnitt":>19}{farbe_ball}""\n")
        print(f"{"Schnitt":>25} = {notendurchschnitt:>4}""\n")
        print(f"{"Ziel":>22} {"=":>4} {noten_ziel:>4}")
        if erklärung: print(erklärung) 

    def print_alle_module(self, modul_liste):
        """Druckt alle Module aus"""
        for modul_info in modul_liste:
            print(modul_info)

    def belegungen(self, anzahl_belegungen, belegungen):
        """Druckt alle bestandenen Belegungen aus"""
        print(f"{f"Insgesamt {anzahl_belegungen} belegungen":^61}{"\n"*2}")
        print(f"{"Modul":^68} | {"Note":^5}| {"Art der Prüfung":^15} | {"Datum":^10}")
        print("-" * 106)
        for i, belegung in enumerate(belegungen, start=1):
            print(f"{belegung.pruefung.modul.name:<68} | {belegung.note:<5}| {belegung.pruefung.pruefungstyp.value:^15} | {belegung.pruefungsdatum}")
