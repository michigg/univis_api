import logging
import re
from typing import List

import requests
import xmltodict
from pyexpat import ExpatError

from models.lecture_models import Lecture
from models.room_models import UnivISRoom

logger = logging.getLogger(__name__)
UNIVIS_SEMESTER = "ws2019"


class UnvISPerson(object):
    pass


class UnivISController:
    def __init__(self):
        self.room_regex = "([a-zA-Z0-9]*)\/([0-9]{2})\.([0-9]{2,3}).*"

    def load_page(self, url: str):
        data = requests.get(url).content
        try:
            return xmltodict.parse(data)
        except ExpatError:
            return None

    # def get_persons(self, data: dict) -> List[UnvISPerson]:
    #     return [UnvISPerson(person) for person in data['UnivIS']['Person'] if 'Person' in data['UnivIS']]

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
        data = {}
        for url in urls:
            univis_data = self.load_page(url)
            if not data:
                data = univis_data
            else:
                if "Person" in data["UnivIS"]:
                    data["UnivIS"]["Person"].extend(univis_data["UnivIS"]["Person"])
                if "Room" in data["UnivIS"]:
                    data["UnivIS"]["Room"].extend(univis_data["UnivIS"]["Room"])
                if "Allocation" in data["UnivIS"]:
                    data["UnivIS"]["Allocation"].extend(univis_data["UnivIS"]["Allocation"])
                if "Lecture" in data["UnivIS"]:
                    data["UnivIS"]["Lecture"].extend(univis_data["UnivIS"]["Lecture"])
        return data

    # def get_rooms_from_data(self, data: List):
    #     logger.error([self.is_a_room(room) for room in data])
    #     return [UnivISRoom(room) for room in data if self.is_a_room(room)]


class UnivISLectureController(UnivISController):
    def __init__(self, semester=UNIVIS_SEMESTER):
        UnivISController.__init__(self)
        self.univis_api_base_url = "http://univis.uni-bamberg.de/prg"
        self.semester = semester

    def _get_univis_api_url(self, lecture_search_token):
        return f'{self.univis_api_base_url}?search=lectures&name={lecture_search_token}&sem={self.semester}&show=xml'

    def get_rooms(self, data: dict) -> List[UnivISRoom]:
        rooms = []
        if 'Room' in data['UnivIS']:
            if type(data['UnivIS']['Room']) is list:
                rooms = self.get_rooms_from_data(data['UnivIS']['Room'])
            else:
                rooms = [UnivISRoom(data['UnivIS']['Room'])] if self.is_a_room(data['UnivIS']['Room']) else []
        return rooms

    def get_lectures(self, data: dict, rooms: List[UnivISRoom]) -> List[Lecture]:
        lectures = []
        if 'Lecture' in data['UnivIS']:
            if type(data['UnivIS']['Lecture']) is list:
                lectures = [Lecture(lecture, rooms) for lecture in data['UnivIS']['Lecture'] if 'terms' in lecture]
            else:
                lectures = [Lecture(data['UnivIS']['Lecture'], rooms)]
        return lectures

    def get_lectures_by_token(self, token: str):
        data = self.load_page(self._get_univis_api_url(token))
        # TODO get lecture by date and time
        if data and 'UnivIS' in data and 'Lecture' in data['UnivIS']:
            lectures = self.get_lectures(data, self.get_rooms(data))
            lecture_map = self.get_univis_key_dict(lectures)
            person_map = self.get_univis_key_dict(self.get_persons(data))
            clean_lectures = []
            for lecture in lectures:
                if len(lecture.terms) > 0:
                    if lecture.parent_lecture__ref:
                        lecture.parent_lecture = lecture_map[lecture.parent_lecture__ref]
                    lecture.lecturers = [person_map[lecturer.univis_key] for lecturer in lecture.lecturers]
                    clean_lectures.append(lecture)

            logger.info(f'FOUND LECTURES {len(clean_lectures)}')
            return clean_lectures
        return []

    # def get_lectures_split_by_date(self, lectures):
    #     current_time = timezone.localtime(timezone.now())
    #     lectures = self.get_lectures_sorted_by_starttime(lectures)
    #     lectures_before = []
    #     lectures_after = []
    #     for lecture in lectures:
    #         if lecture.get_last_term().starttime.time() < current_time.time():
    #             lectures_before.append(lecture)
    #         else:
    #             lectures_after.append(lecture)
    #     return lectures_after, lectures_before

    def get_lectures_sorted_by_starttime(self, lectures):
        return sorted(lectures, key=lambda lecture: lecture.get_first_term().starttime)
