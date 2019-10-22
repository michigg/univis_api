from typing import List
from urllib.parse import urlencode, quote_plus

from models.enums.building_key import BuildingKey
from models.enums.faculty import Faculty
from models.room_models import UnivISRoom
from utils.controllers import UnivISController

UnivISRoomKeys = ['k', 'z', 'u', 'w', 'f', 'r', 'h', 'l', 'm', 'o', 'p', 'v', 'd', 'x']


class UnivISRoomController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = "http://univis.uni-bamberg.de/prg"

    def get_univis_api_url(self, token: str = None,
                           name: str = None,
                           long_name: str = None,
                           size: int = None,
                           id: int = None,
                           faculty: Faculty = None,
                           building_key: BuildingKey = None):
        params = {"search": "rooms", "show": "xml"}
        if token:
            params['name'] = token
        if name:
            params['name'] = name
        if building_key:
            params['name'] = building_key.value
        if long_name:
            params['longname'] = long_name
        if size:
            params['size'] = size
        if id:
            params['id'] = id
        if faculty:
            params['department'] = faculty.value
        return f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}'

    def extract_rooms(self, data: dict) -> List[UnivISRoom]:
        return self.get_rooms_from_data(data['UnivIS']['Room']) if 'Room' in data['UnivIS'] else []

    def get_rooms(self, url=None):
        if url:
            data = self.load_page(url)
            return self.extract_rooms(data) if data else []
        else:
            rooms = []
            for key in UnivISRoomKeys:
                rooms.extend(self.get_tokens_rooms(key))
            return list(set(rooms))

    # def get_building_keys_rooms(self, building_key: str) -> List[UnivISRoom]:
    #     data = self.load_page(self._get_univis_api_url(building_key))
    #     rooms = self.get_rooms_from_data(data['UnivIS']['Room'])
    #     return [room for room in rooms if building_key.lower() in room.building_key.lower()] if 'Room' in data[
    #         'UnivIS'] else []
    def get_tokens_rooms(self, token) -> List[UnivISRoom]:
        data = self.load_page(self.get_univis_api_url(token))
        return self.extract_rooms(data) if data else []
