from typing import List

from models.base import UnivISBase
from models.room_models import Room


class UnivISPerson(UnivISBase):
    def __init__(self, univis_person: dict):
        self.id = univis_person.get('id', None)
        self.univis_key = univis_person.get('@key')
        self.first_name = univis_person.get('firstname', None)
        self.last_name = univis_person.get('lastname', None)
        self.title = univis_person.get('atitle', None)
        self.gender = univis_person.get('gender', None)
        self.orgname = univis_person.get('orgname', None)
        self.orgunits = self._get_orgunits(univis_person)
        self.work = univis_person.get('work', None)
        # TODO implement office hours
        raw_office_hours = univis_person.get('office_hours', None)
        self.office_hours = self._get_office_hours(raw_office_hours) if raw_office_hours else None
        self.locations = self._get_locations(univis_person) if 'locations' in univis_person else None

        self.visible = True if univis_person.get('visible', "nein") == "ja" else False
        self.pub_visible = True if univis_person.get('pub_visible', "nein") == "ja" else False

        self.lehr = True if univis_person.get('lehr', "nein") == "ja" else False
        self.lehr_typ = univis_person.get('lehrtyp')

    def _get_office_hours(self, univis_office_hours: List[dict]):
        return [UnivISOfficeHour(univis_office_hour) for univis_office_hour in univis_office_hours]

    def _get_locations(self, univis_person: dict):
        if type(univis_person['locations']['location']) is list:
            return [UnivISLocation(univis_location) for univis_location in univis_person['locations']['location'] if
                    "office" in univis_location]
        return UnivISLocation(univis_person['locations']['location'])

    def __str__(self):
        return f'Person {self.first_name} {self.last_name}\n\tUnivis Key {self.univis_key}\n\tTitle {self.title}\n\tGender {self.gender}'


class UnivISOfficeHour:
    def __init__(self, univis_office_hour: dict):
        self.start_time = univis_office_hour.get('starttime', None)
        self.end_time = univis_office_hour.get('endtime', None)
        self.repeat = univis_office_hour.get('repeat', None)
        self.office = univis_office_hour.get('office', None)


class UnivISLocation(Room):
    def __init__(self, univis_room):
        building_key, floor, number = self._init_room_number(univis_room)
        Room.__init__(self, building_key, floor, number)
        self.street = univis_room.get('street', None)
        self.phone = univis_room.get('tel', None)
        self.url = univis_room.get('url', None)
        self.fax = univis_room.get('fax', None)
        self.email = univis_room.get('email', None)
        self.location = univis_room.get('ort', None)

    @staticmethod
    def _init_room_number(univis_room) -> (str, int, int):
        splitted_room_id = str(univis_room['office']).split('/')
        splitted_room_number = splitted_room_id[1].split('.')
        building_key = splitted_room_id[0]
        level = int(splitted_room_number[0])
        number = int(splitted_room_number[1])
        return building_key, level, number

    def __eq__(self, other):
        return self.building_key == other.building_key \
               and self.number == other.number \
               and self.floor == other.floor

    def __str__(self):
        return f'{self.building_key}/{self.floor:02d}.{self.number:03d}'
