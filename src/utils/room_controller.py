import os
from typing import List
from urllib.parse import urlencode, quote_plus

from models.enums.building_key import BuildingKey
from models.enums.faculty import Faculty
from models.room_models import UnivISRoom
from utils.controllers import UnivISController

UNIVIS_ROOM_KEYS = os.environ.get("UNIVIS_ROOM_KEYS").split(",")


class UnivISRoomController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = os.environ.get("UNIVIS_API_ENDPOINT")

    def get_url(self, args) -> str:
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
            building_keys_str = "|".join(building_key_strings) if building_key_strings else ""
            params['name'] = building_keys_str
        return f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}'

    def get_univis_data_rooms(self, urls: List[str]) -> List[UnivISRoom]:
        rooms = []
        for url in urls:
            univis_data = self.load_page(url)
            rooms.extend(self._extract_rooms(univis_data))
        return rooms

    def get_all_rooms_urls(self):
        return [self.get_url({"token": key}) for key in UNIVIS_ROOM_KEYS]

    def _extract_rooms(self, univis_data: dict) -> List[UnivISRoom]:
        univis_rooms = self._get_univis_rooms_from_univis_data(univis_data)

        if type(univis_rooms) is list:
            rooms = []
            for univis_room in univis_rooms:
                room = self._extract_room(univis_room)
                if room:
                    rooms.append(room)
            return rooms
        else:
            return [self._extract_room(univis_rooms)]

    def _extract_room(self, univis_room: dict) -> UnivISRoom or None:
        return UnivISRoom(univis_room) if self.is_a_room(univis_room) else None

    def _get_univis_rooms_from_univis_data(self, univis_data: dict) -> List[dict] or None:
        if 'UnivIS' in univis_data:
            return univis_data['UnivIS']['Room'] if 'Room' in univis_data['UnivIS'] else None
        return None

    def get_enum(self, enum, key: str):
        result = [member for name, member in enum.__members__.items() if str(member.name).lower() == key.lower()]
        return result[0] if result else None
