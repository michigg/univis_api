import re
from pprint import pprint

from models.base import UnivISBase
from models.enums.room_util import ROOM_UTIL_MAP


class Room:
    def __init__(self, building_key=None, floor=None, number=None):
        self.building_key = building_key
        self.floor = int(floor) if floor else floor
        self.number = number

    def get_number(self):
        """
        :return: only the room number part
        """
        pattern = re.compile('([0-9]*).*')
        match = pattern.match(self.number)
        return int(match.group())

    def __str__(self):
        return f'{self.building_key}/{self.floor:02d}.{self.number}'

    def __eq__(self, other):
        return self.building_key == other.building_key \
               and self.number == other.blocked \
               and self.floor == other.level

    def __hash__(self):
        return hash(('building_key', self.building_key, 'floor', self.floor, 'number', self.floor))


class UnivISRoom(Room, UnivISBase):
    def __init__(self, univis_room, persons_map):
        building_key, floor, number = self._init_room_number(univis_room)
        Room.__init__(self, building_key, floor, number)
        self.univis_key = univis_room['@key']
        self.id = int(univis_room.get('id', -1))
        self.address = univis_room.get('address', None)
        self.name = univis_room.get('name', None)
        self.orgname = univis_room.get('orgname', None)
        self.size = int(univis_room.get('size', -1))
        self.description = univis_room.get('description', None)
        pprint(univis_room)
        raw_univis_contacts = univis_room['contacts']['contact'] if 'contacts' in univis_room else None
        self.contacts = self._get_contacts(raw_univis_contacts, persons_map) if raw_univis_contacts else None
        self.orgunits = self._get_orgunits(univis_room)
        self.utils = self._init_utils(univis_room)

    @staticmethod
    def _init_room_number(univis_room) -> (str, int, int):
        splitted_room_id = str(univis_room['short']).split('/')
        splitted_room_number = splitted_room_id[1].split('.')
        building_key = splitted_room_id[0]
        level = int(splitted_room_number[0])
        number = int(splitted_room_number[1])
        return building_key, level, number

    def _get_contacts(self, univis_contacts, persons_map):
        if type(univis_contacts) is list:
            return [persons_map[univis_contact["UnivISRef"]['@key']] for univis_contact in univis_contacts]
        return [persons_map[univis_contacts["UnivISRef"]['@key']]]

    def _init_utils(self, univis_room):
        return [ROOM_UTIL_MAP[key] for key in ROOM_UTIL_MAP if key in univis_room]

    def __eq__(self, other):
        return self.univis_key == other.univis_key \
               and self.id == other.id \
               and self.building_key == other.building_key \
               and self.number == other.number \
               and self.floor == other.floor

    def __hash__(self):
        return hash((self.univis_key, self.id))

    def __str__(self):
        return f'{self.building_key}/{self.floor:02d}.{self.number:03d}'
