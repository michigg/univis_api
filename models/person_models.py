class Person:
    def __init__(self, univis_person: dict):
        self.univis_key = univis_person.get('@key')
        self.title = univis_person.get('atitle', None)
        self.first_name = univis_person.get('firstname')
        self.last_name = univis_person.get('lastname')
        self.gender = univis_person.get('gender')
        self.id = univis_person.get('id')
        self.pub_visible = True if univis_person.get('pub_visible', "nein") == "ja" else False
        self.visible = True if univis_person.get('visible', "nein") == "ja" else False

    def __str__(self):
        return f'Person {self.first_name} {self.last_name}\n\tUnivis Key {self.univis_key}\n\tTitle {self.title}\n\tGender {self.gender}'