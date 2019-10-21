import datetime
from typing import List

from models.enums.lecture_type import LectureType
from models.room_models import UnivISRoom
from models.person_models import Person


class LectureTerm:
    def __init__(self, univis_term: dict, rooms: List[UnivISRoom]):
        self.starttime = datetime.datetime.strptime(univis_term.get('starttime'), '%H:%M')
        self.endtime = datetime.datetime.strptime(univis_term.get('endtime'), '%H:%M')
        self.repeat = univis_term.get('repeat')
        self.room = rooms


class Lecture:
    def __init__(self, univis_lecture: dict, rooms: List[UnivISRoom]):
        terms = [term[1] for term in list(univis_lecture['terms'].items())][0]
        terms = [dict(term) for term in terms] if type(terms) is list else [dict(terms)]
        dozs = []
        if 'dozs' in univis_lecture:
            dozs = [doz[1] for doz in list(univis_lecture['dozs'].items())][0]
            dozs = [dict(doz['UnivISRef']) for doz in dozs] if type(dozs) is list else [dict(dozs['UnivISRef'])]

        self.univis_key = univis_lecture.get('@key')
        self._init_lecture_terms(rooms, terms)
        self.type = self._get_type(univis_lecture.get('type'))
        self.lecturers = [Person(lecturer) for lecturer in dozs]
        self.name = univis_lecture.get('name')
        self.orgname = univis_lecture.get('orgname')
        self.parent_lecture__ref = univis_lecture['parent-lv']['UnivISRef']['@key'] if univis_lecture.get('parent-lv',
                                                                                                          None) else None
        self.parent_lecture = None

    def _init_lecture_terms(self, rooms, terms):
        lecture_terms = []
        for term in terms:
            if 'room' in term:
                rooms = list(filter(lambda x: x.univis_key == dict(term['room']['UnivISRef']).get('@key'), rooms))
                if rooms:
                    lecture_terms.append(LectureTerm(term, rooms[0]))
        self.terms = lecture_terms

    @staticmethod
    def _get_type(univis_type: str) -> LectureType or None:
        types = {'V': LectureType.LECTURE, 'Ü': LectureType.EXERCISE, 'TU': LectureType.TUTORIUM,
                 'S': LectureType.SEMINAR, 'SL': LectureType.FURTHER_LECTURE, 'S/PS': LectureType.SEMINAR_PRO_SEMINAR,
                 'PS/Ü': LectureType.PRO_SEMINAR_EXERCISE, 'PS': LectureType.PRO_SEMINAR,
                 'V/S': LectureType.LECTURE_SEMINAR, 'S/Ü': LectureType.SEMINAR_EXERCISE,
                 'GK': LectureType.BASIC_COURSE, 'Q/Ü': LectureType.SOURCE_STUDY_EXERCISE,
                 'PS/HS': LectureType.PRO_SEMINAR_MAIN_SEMINAR, 'S/PS/Ü': LectureType.SEMINAR_PRO_SEMINAR_EXERCISE,
                 'V/Ü': LectureType.LECTURE_EXERCISE, 'Ü/T': LectureType.EXERCISE_TUTORIUM,
                 'BS': LectureType.BLOCK_SEMINAR, 'Ü/BS': LectureType.EXERCISE_BLOCK_SEMINAR,
                 'HS': LectureType.MAIN_SEMINAR, 'K': LectureType.COURSE, 'SA': LectureType.LANGUAGE_TRAINING,
                 'V/SP': LectureType.LECTURE_WITH_STUDYACCOMPANYING_EXAMINATION, 'GS': LectureType.TERRAIN_SEMINAR,
                 'PROJ': LectureType.PROJECT, 'PUE': LectureType.PRAKTIKUM_EXERCISE}

        return types[univis_type] if univis_type in types else None

    def get_first_term(self) -> List[LectureTerm] or None:
        sorted_terms = self._get_sorted_terms()
        return sorted_terms[0] if len(sorted_terms) > 0 else None

    def get_last_term(self) -> List[LectureTerm] or None:
        sorted_terms = self._get_sorted_terms()
        return sorted_terms[-1] if len(sorted_terms) > 0 else None

    def _get_sorted_terms(self) -> List[LectureTerm]:
        return sorted(self.terms, key=lambda x: x.starttime)

    def get_rooms(self):
        return [term.room for term in self.terms]

    def __str__(self):
        if self.parent_lecture:
            return f'Lecture {self.name}:\n\tUnivIS Key: {self.univis_key}\n\tType: {self.type}\n\tOrgname: {self.orgname}\n\tParent Lecture: {self.parent_lecture.name}\n\tROOMS: {self.get_rooms()}'
        else:
            return f'Lecture {self.name}:\n\tUnivIS Key: {self.univis_key}\n\tType: {self.type}\n\tOrgname: {self.orgname}\n\tParent Lecture Ref: {self.parent_lecture__ref}\n\tROOMS: {self.get_rooms()}'
