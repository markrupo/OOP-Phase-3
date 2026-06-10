import json
from EntityKlassen import *

def speichern(student, studiengang):
    data = {
        "student": {
            "name": student.name,
            "anmeldedatum": student.anmeldedatum.isoformat(),
            "belegungen": [
                {
                    "note": belegung.note,
                    "pruefungstyp": belegung.pruefung.pruefungstyp.value,
                    "pruefungsdatum": belegung.pruefungsdatum.isoformat()
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
        return data