import json
from datetime import datetime

class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
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
        
    @staticmethod
    def load_by_id(ID):
        '''A function that loads a person by id and returns the person as a dictionary.'''
        person_data = Person.load_person_data()

        if ID == "None":
            return None

        for eintrag in person_data:
            if eintrag["id"] == ID:
                return eintrag
        else:
            return {}
        
    def get_personIDs(person_data):
        '''A function that returns a list of all person IDs.'''
        list_of_ids = []

        for eintrag in person_data:
            list_of_ids.append(eintrag["id"])
        return list_of_ids
    
    """def get_new_id(list_of_ids):
        '''A function that returns a new ID for a person.'''
        new_id = max(list_of_ids) + 1
        return new_id"""
    
    @staticmethod
    def get_new_id(list_of_ids):
        '''A function that returns a new ID for a person.'''
        if not list_of_ids:
            return 1
        else:
            return max(list_of_ids) + 1
        
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]

    def calc_age(self):
        '''A function that calculates the age of a person based on the date of birth.'''

        today = datetime.today()
        age = today.year - self.date_of_birth
        
        return age


    def calc_max_heart_rate(self):
        '''A function that calculates the maximum heart rate of a person.'''

        age = self.calc_age()
        max_heart_rate = 220 - age

        return max_heart_rate
    
    
    



if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    print(type(persons))
    
    person_names = Person.get_person_list(persons)
    person1 = Person(Person.find_person_data_by_name("Huber, Julian"))