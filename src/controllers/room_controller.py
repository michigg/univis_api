import os
from pprint import pprint
from typing import List
from urllib.parse import urlencode, quote_plus

from controllers.controllers import UnivISController
from controllers.person_controller import UnivISPersonController
from models.enums.building_key import BuildingKey
from models.enums.faculty import Faculty
from models.room_models import UnivISRoom

UNIVIS_ROOM_KEYS = os.environ.get("UNIVIS_ROOM_KEYS").split(",")


class UnivISRoomController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = os.environ.get("UNIVIS_API_ENDPOINT")

    def get_urls(self, args) -> List[str]:
        urls = []
        params = {"search": "rooms", "show": "xml"}
        if "id" in args and args["id"]:
            params['id'] = args["id"]
        if "token" in args and args["token"]:
            params['name'] = args["token"]
        if "name" in args and args["name"]:
            params['name'] = args["name"]
        if "long_name" in args and args["long_name"]:
            params['longname'] = args["long_name"]
        if "size" in args and args["size"]:
            params['size'] = args["size"]
        if "faculty" in args and args["faculty"]:
            faculty_enum = self.get_enum(Faculty, args["faculty"])
            if faculty_enum:
                params['department'] = faculty_enum.value
        if "building_keys" in args and args["building_keys"]:
            building_key_enums = [self.get_enum(BuildingKey, building_key) for building_key in args["building_keys"] if
                                  building_key]
            building_key_strings = [building_key.value for building_key in building_key_enums]
            for building_key_string in building_key_strings:
                copied_params = params.copy()
                copied_params["name"] = building_key_string
                urls.append(f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}')
            return urls
        return [f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}']

    def get_rooms(self, univis_data: dict) -> List[UnivISRoom]:
        univis_person_c = UnivISPersonController()
        persons = univis_person_c.get_persons(univis_data)
        persons_map = self.get_univis_key_dict(persons)
        return self.extract_rooms(univis_data=univis_data, persons_map=persons_map)

    def extract_rooms(self, univis_data: dict, persons_map: dict):
        rooms = []
        if 'UnivIS' in univis_data:
            univis_rooms = univis_data['UnivIS']['Room'] if 'Room' in univis_data['UnivIS'] else None
            if univis_rooms:
                if type(univis_rooms) is list:
                    for univis_room in univis_rooms:
                        room = self._extract_room(univis_room, persons_map)
                        if room:
                            rooms.append(room)
                else:
                    rooms = [self._extract_room(univis_rooms, persons_map)]
        return rooms

    def get_all_rooms_urls(self):
        return [self.get_urls({"token": key})[0] for key in UNIVIS_ROOM_KEYS]

    def _extract_room(self, univis_room: dict, persons_map: dict) -> UnivISRoom or None:
        return UnivISRoom(univis_room, persons_map) if self.is_a_room(univis_room) else None

    def get_enum(self, enum, key: str):
        result = [member for name, member in enum.__members__.items() if str(member.name).lower() == key.lower()]
        return result[0] if result else None
