import re
from enum import Enum


class RoomUtil(str, Enum):
    BEAM: str = "Projektor"
    DBEAM: str = "Doppelprojektion"
    OHEAD: str = "Overheadprojektor"
    DARK: str = "Verdunkelung"
    LOSE: str = "lose Bestuhlung"
    SMART: str = "Interaktive Tafel"
    VISU: str = "DocCam"
    MIKR: str = "Pultmikrofon"
    PC: str = "Interner PC"
    BLUERAY: str = "Blu-Ray Player"
    DVD: str = "DVD Player"
    PRUEF: str = "Prüfungsraum"


ROOM_UTIL_MAP = {"beam": RoomUtil.BEAM, "dbeam": RoomUtil.DBEAM, "ohead": RoomUtil.OHEAD, "dark": RoomUtil.DARK,
                 "lose": RoomUtil.LOSE, "smart": RoomUtil.SMART, "visu": RoomUtil.VISU, "mikr": RoomUtil.MIKR,
                 "pc": RoomUtil.PC, "blueray": RoomUtil.BLUERAY, "dvd": RoomUtil.DVD, "pruef": RoomUtil.PRUEF}


class Room:
    def __init__(self, building_key=None, floor=None, number=None):
        self.building_key = building_key
        self.number = number
        self.floor = int(floor)

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


class UnivISRoom(Room):
    def __init__(self, univis_room):
        building_key, floor, number = self._init_room_number(univis_room)
        Room.__init__(self, building_key, floor, number)
        self.univis_key = univis_room['@key']
        self.id = int(univis_room.get('id', -1))
        self.address = univis_room.get('address', None)
        self.name = univis_room.get('name', None)
        self.orgname = univis_room.get('orgname', None)
        self.size = int(univis_room.get('size', -1))
        self.description = univis_room.get('description', None)
        # TODO: Contacts
        self.contacts = []
        self.orgunits = self._init_orgunits(univis_room)
        self.utils = self._init_utils(univis_room)

    @staticmethod
    def _init_room_number(univis_room) -> (str, int, int):
        splitted_room_id = str(univis_room['short']).split('/')
        splitted_room_number = splitted_room_id[1].split('.')
        building_key = splitted_room_id[0]
        level = int(splitted_room_number[0])
        number = int(splitted_room_number[1])
        return building_key, level, number

    def _init_utils(self, univis_room):
        return [ROOM_UTIL_MAP[key] for key in ROOM_UTIL_MAP if key in univis_room]

    def _init_orgunits(self, univis_room):
        if len(univis_room['orgunits']) > 1:
            return [orgunit for orgunit in univis_room['orgunits']['orgunit']]
        return univis_room['orgunits']['orgunit']

    def __str__(self):
        return f'{self.building_key}/{self.floor:02d}.{self.number:03d}'
