import logging
import re
from typing import List

import requests
import xmltodict
from pyexpat import ExpatError

from models.lecture_models import UnivISLecture
from models.room_models import UnivISRoom

logger = logging.getLogger(__name__)
UNIVIS_SEMESTER = "ws2019"


class UnvISPerson(object):
    pass


class UnivISController:
    def __init__(self):
        self.room_regex = "([a-zA-ZäöüÄÖÜ0-9]*)\/([0-9]{2})\.([0-9]{2,3}).*"

    def load_page(self, url: str):
        data = requests.get(url).content
        try:
            return xmltodict.parse(data)
        except ExpatError:
            return None

    def is_a_room(self, room: dict):
        try:
            if 'short' in room:
                return re.match(self.room_regex, room['short'])
            else:
                return re.match(self.room_regex, room['office'])
        except TypeError:
            return False

    def get_univis_key_dict(self, objects):
        map = {}
        for object in objects:
            map[object.univis_key] = object
        return map

    def get_data(self, urls: List[str]) -> dict:
        data = {"UnivIS": {}}
        for url in urls:
            univis_data = self.load_page(url)
            if not data:
                data = univis_data
            else:
                if "Person" in univis_data["UnivIS"]:
                    persons = univis_data["UnivIS"]["Person"] if type(
                        univis_data["UnivIS"]["Person"]) == list else [univis_data["UnivIS"]["Person"]]
                    if "Person" in data["UnivIS"]:
                        data["UnivIS"]["Person"].extend(persons)
                    else:
                        data["UnivIS"]["Person"] = persons
                if "Room" in univis_data["UnivIS"]:
                    rooms = univis_data["UnivIS"]["Room"] if type(
                        univis_data["UnivIS"]["Room"]) == list else [univis_data["UnivIS"]["Room"]]
                    if "Room" in data["UnivIS"]:
                        data["UnivIS"]["Room"].extend(rooms)
                    else:
                        data["UnivIS"]["Room"] = rooms
                if "Allocation" in univis_data["UnivIS"]:
                    allocations = univis_data["UnivIS"]["Allocation"] if type(
                        univis_data["UnivIS"]["Allocation"]) == list else [univis_data["UnivIS"]["Allocation"]]
                    if "Allocation" in data["UnivIS"]:
                        data["UnivIS"]["Allocation"].extend(allocations)
                    else:
                        data["UnivIS"]["Allocation"] = allocations
                if "Lecture" in univis_data["UnivIS"]:
                    lectures = univis_data["UnivIS"]["Lecture"] if type(
                        univis_data["UnivIS"]["Lecture"]) == list else [univis_data["UnivIS"]["Lecture"]]
                    if "Allocation" in data["UnivIS"]:
                        data["UnivIS"]["Lecture"].extend(lectures)
                    else:
                        data["UnivIS"]["Lecture"] = lectures
        return data
