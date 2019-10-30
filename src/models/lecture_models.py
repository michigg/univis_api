import datetime
from pprint import pprint
from typing import List

from models.base import UnivISBase
from models.enums.lecture_type import LectureType


class LectureTerm:
    def __init__(self, univis_term: dict, rooms_map: dict):
        self.starttime = datetime.datetime.strptime(univis_term.get('starttime'),
                                                    '%H:%M') if 'starttime' in univis_term else None
        self.endtime = datetime.datetime.strptime(univis_term.get('endtime'),
                                                  '%H:%M') if 'endtime' in univis_term else None
        self.repeat = univis_term.get('repeat', None)
        univis_room_key = univis_term['room']["UnivISRef"]["@key"] if "room" in univis_term else None
        self.room = rooms_map[univis_room_key] if univis_room_key else None


class UnivISLecture(UnivISBase):
    def __init__(self, univis_lecture: dict, rooms_map: dict, persons_map: dict):
        self.univis_key = univis_lecture.get('@key')
        self.id = univis_lecture.get('id')

        raw_univis_doz = univis_lecture['dozs']['doz'] if 'dozs' in univis_lecture else None
        self.dozs = self._get_contacts(raw_univis_doz, persons_map)[0] if raw_univis_doz else []

        self.ects = True if univis_lecture.get('ects', "nein") == "ja" else False
        self.ects_cred = univis_lecture.get('ects_cred')
        self.english = True if univis_lecture.get('english', "nein") == "ja" else False
        self.name = univis_lecture.get('name', None)
        self.orgname = univis_lecture.get('orgname', None)
        self.orgunits = self._get_orgunits(univis_lecture)
        self.organizational = univis_lecture.get('organizational', None)
        self.summary = univis_lecture.get('summary', None)
        self.sws = univis_lecture.get('sws', None)
        self.turnout = univis_lecture.get('turnout', None)

        raw_univis_terms = univis_lecture['terms']['term'] if 'terms' in univis_lecture else []
        self.terms = self._get_lecture_terms(rooms_map=rooms_map, terms=raw_univis_terms)

        self.time_description = univis_lecture.get('time_description', None)
        self.type = self._get_type(univis_lecture.get('type', None))
        # TODO implement
        # self.classification = None
        # TODO implement
        self.parent_lecture_ref = univis_lecture['parent-lv']['UnivISRef']['@key'] if univis_lecture.get('parent-lv',
                                                                                                         None) else None
        print(self.parent_lecture_ref)
        self.parent_lecture = None

    def _get_lecture_terms(self, rooms_map: dict, terms):
        if terms:
            if type(terms) == list:
                return [LectureTerm(univis_term=term, rooms_map=rooms_map) for term in terms]
            else:
                return [LectureTerm(univis_term=terms, rooms_map=rooms_map)]

    @staticmethod
    def _get_type(univis_type: str) -> LectureType or None:
        types = {'V': LectureType.LECTURE,
                 'Ü': LectureType.EXERCISE,
                 'TU': LectureType.TUTORIUM,
                 'S': LectureType.SEMINAR,
                 'SL': LectureType.FURTHER_LECTURE,
                 'S/PS': LectureType.SEMINAR_PRO_SEMINAR,
                 'PS/Ü': LectureType.PRO_SEMINAR_EXERCISE,
                 'PS': LectureType.PRO_SEMINAR,
                 'V/S': LectureType.LECTURE_SEMINAR,
                 'S/Ü': LectureType.SEMINAR_EXERCISE,
                 'GK': LectureType.BASIC_COURSE,
                 'Q/Ü': LectureType.SOURCE_STUDY_EXERCISE,
                 'PS/HS': LectureType.PRO_SEMINAR_MAIN_SEMINAR,
                 'S/PS/Ü': LectureType.SEMINAR_PRO_SEMINAR_EXERCISE,
                 'V/Ü': LectureType.LECTURE_EXERCISE,
                 'Ü/T': LectureType.EXERCISE_TUTORIUM,
                 'BS': LectureType.BLOCK_SEMINAR,
                 'Ü/BS': LectureType.EXERCISE_BLOCK_SEMINAR,
                 'HS': LectureType.MAIN_SEMINAR,
                 'K': LectureType.COURSE,
                 'SA': LectureType.LANGUAGE_TRAINING,
                 'V/SP': LectureType.LECTURE_WITH_STUDYACCOMPANYING_EXAMINATION,
                 'GS': LectureType.TERRAIN_SEMINAR,
                 'PROJ': LectureType.PROJECT,
                 'PUE': LectureType.PRAKTIKUM_EXERCISE}

        return str(types[univis_type]) if univis_type in types else None

    # def get_first_term(self) -> List[LectureTerm] or None:
    #     sorted_terms = self._get_sorted_terms()
    #     return sorted_terms[0] if len(sorted_terms) > 0 else None
    #
    # def get_last_term(self) -> List[LectureTerm] or None:
    #     sorted_terms = self._get_sorted_terms()
    #     return sorted_terms[-1] if len(sorted_terms) > 0 else None

    def _get_sorted_terms(self) -> List[LectureTerm]:
        return sorted(self.terms, key=lambda x: x.starttime)

    # def get_rooms(self):
    #     return [term.room for term in self.terms]

    def set_parent_lecture(self, lectures_map: dict):
        if self.parent_lecture_ref:
            self.parent_lecture = lectures_map[self.parent_lecture_ref]

    def __str__(self):
        if self.parent_lecture:
            return f'Lecture {self.name}:\n\tUnivIS Key: {self.univis_key}\n\tType: {self.type}\n\tOrgname: {self.orgname}\n\tParent Lecture: {self.parent_lecture.name}\n\tROOMS: {self.get_rooms()}'
        else:
            return f'Lecture {self.name}:\n\tUnivIS Key: {self.univis_key}\n\tType: {self.type}\n\tOrgname: {self.orgname}\n\tParent Lecture Ref: {self.parent_lecture__ref}\n\tROOMS: {self.get_rooms()}'
