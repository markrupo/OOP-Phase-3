import json
from EntityKlassen import *
from datetime import datetime

class daten_manager:
    def speichern(student, studiengang):
        """Speichert Student und Studiengang im JSON Format"""
        data = {
            "student": {
                "name": student.name,
                "anmeldedatum": student.anmeldedatum.isoformat(),
                "noten_ziel": student.noten_ziel,
                "zeit_ziel": student.zeit_ziel,
                "belegungen": [
                    {
                        "note": belegung.note,
                        "pruefungsdatum": belegung.pruefungsdatum.isoformat(),
                        "pruefung": {
                            "pruefungstyp": belegung.pruefung.pruefungstyp.value,
                            "modul": {
                                "name": belegung.pruefung.modul.name,
                                "ects": belegung.pruefung.modul.ects
                            }
                        }
                    }
                    for belegung in student.belegungen
                ]
            },
            "studiengang": {
                "name": studiengang.name,
                "ects": studiengang.ects,
                "module": [
                    {"name": modul.name, "ects": modul.ects}
                    for modul in studiengang.module
                ]
            }
        }

        with open("student_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    def laden():
        """Stellt Student und Studiengang als Objekte wieder her"""
        with open("student_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        
        studiengang = Studiengang(data["studiengang"]["name"], data["studiengang"]["ects"])

        for modul in data["studiengang"]["module"]:
            m = Modul(modul["name"], modul["ects"])
            studiengang.module.append(m)

        
        student = Student(data["student"]["name"], datetime.fromisoformat(data["student"]["anmeldedatum"]).date(), data["student"]["noten_ziel"], data["student"]["zeit_ziel"])

        for belegung in data["student"]["belegungen"]:
            index = 0
            for modul in studiengang.module:
                if modul.name == belegung["pruefung"]["modul"]["name"]:
                    index += studiengang.module.index(modul)
                    p = Pruefung(Pruefungstyp(belegung["pruefung"]["pruefungstyp"]), studiengang.module[index])
                    b = Belegung(belegung["note"], p, datetime.fromisoformat(belegung["pruefungsdatum"]).date())
                    student.belegungen.append(b)
                
        return student, studiengang
