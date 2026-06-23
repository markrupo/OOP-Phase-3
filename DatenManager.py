import json
from EntityKlassen import *
from datetime import datetime


def speichern(student, studiengang):
    data = {
        "student": {
            "name": student.name,
            "anmeldedatum": student.anmeldedatum.isoformat(),
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
    with open("student_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    #studiengang wiederherstellung
    studiengang = Studiengang(data["studiengang"]["name"], data["studiengang"]["ects"])

    for modul in data["studiengang"]["module"]:
        m = Modul(modul["name"], modul["ects"])
        studiengang.module.append(m)

    #student wiederherstellung
    student = Student(data["student"]["name"], datetime.fromisoformat(data["student"]["anmeldedatum"]))

    for belegung in data["student"]["belegungen"]:
        index = 0
        for modul in studiengang.module:
            if modul.name == belegung["pruefung"]["modul"]["name"]:
                index += studiengang.module.index(modul)
                p = Pruefung(Pruefungstyp(belegung["pruefung"]["pruefungstyp"]), studiengang.module[index])
                b = Belegung(belegung["note"], p, datetime.fromisoformat(belegung["pruefungsdatum"]))
                student.belegungen.append(b)
            
    return student, studiengang
