#%% Import
import json
import pandas as pd

# Opening JSON file
def load_person_data():
    """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data
# %%

def get_person_list(person_data):
    """A Function that takes the Persons-Dictionary and returns a List auf all person names"""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return list_of_names



# %% Test
#get_person_list(load_person_data())


# %%

def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""
    
    person_data = load_person_data()
    
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
    
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            

            return eintrag
    else:
        return {}


def update_person_data(person_dict):
    """Eine Funktion, die ein Dictionary einer Person entgegennimmt und die Daten in der Datenbank aktualisiert"""
    person_data = load_person_data()
    for i, eintrag in enumerate(person_data):
        if eintrag["id"] == person_dict["id"]:
            person_data[i] = person_dict
            break

    with open("data/person_db.json", "w") as file:
        json.dump(person_data, file, indent=4)
