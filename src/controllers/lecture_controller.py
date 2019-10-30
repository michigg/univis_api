import os
from typing import List
from urllib.parse import urlencode, quote_plus

from controllers.controllers import UnivISController
from controllers.person_controller import UnivISPersonController
from controllers.room_controller import UnivISRoomController
from models.allocation_models import UnivISAllocation
from models.lecture_models import UnivISLecture


class UnivISLectureController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = os.environ.get("UNIVIS_API_ENDPOINT")

    def get_urls(self, args) -> List[str]:
        params = {"search": "lectures", "show": "xml"}
        if "department" in args and args["department"]:
            params['department'] = args["department"]
        if "chapter" in args and args["chapter"]:
            params['chapter'] = args["chapter"]
        if "name" in args and args["name"]:
            params['name'] = args["name"]
        if "short_name" in args and args["short_name"]:
            params['shortname'] = args["short_name"]
        if "type" in args and args["type"]:
            params['type'] = args["type"]
        if "number" in args and args["number"]:
            params['number'] = args["number"]
        if "sws" in args and args["sws"]:
            params['sws'] = args["sws"]
        if "bonus_points" in args and args["bonus_points"]:
            params['bonus'] = args["bonus_points"]
        if "malus_points" in args and args["malus_points"]:
            params['malus'] = args["malus_points"]
        if "ects_credits" in args and args["ects_credits"]:
            params['ectscredits'] = args["ects_credits"]
        if "lecturer" in args and args["lecturer"]:
            params['lecturer'] = args["lecturer"]
        if "room_short" in args and args["room_short"]:
            params['room'] = args["room_short"]
        if "path" in args and args["path"]:
            params['path'] = args["path"]
        if "token" in args and args["token"]:
            params['token'] = args["token"]
        if "token_reg" in args and args["token_reg"]:
            params['tokenreg'] = args["token_reg"]
        if "token_attr" in args and args["token_attr"]:
            params['tokenattr'] = args["token_attr"]
        if "token_sem" in args and args["token_sem"]:
            params['tokensem'] = args["token_sem"]
        if "id" in args and args["id"]:
            params['id'] = args["id"]
        if "evaluation" in args and args["evaluation"]:
            params['evaluation'] = args["evaluation"]
        if "allocation" in args and args["allocation"]:
            params['allocation'] = args["allocation"]
        if "no_imports" in args and args["no_imports"]:
            params['noimports'] = args["no_imports"]
        if "no_subchap" in args and args["no_subchap"]:
            params['nosubchap'] = args["no_subchap"]
        if "no_titles" in args and args["no_titles"]:
            params['notitles'] = args["no_titles"]

        urls = [f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}']
        print(urls)
        return urls

    def get_lectures(self, univis_data: dict) -> List[UnivISLecture]:
        univis_person_c = UnivISPersonController()
        persons = univis_person_c.get_persons(univis_data)
        persons_map = self.get_univis_key_dict(persons)

        univis_room_c = UnivISRoomController()
        rooms = univis_room_c.extract_rooms(univis_data=univis_data, persons_map=persons_map)
        rooms_map = self.get_univis_key_dict(rooms)

        lectures = []
        if 'UnivIS' in univis_data:
            univis_lectures = univis_data['UnivIS']['Lecture'] if 'Lecture' in univis_data['UnivIS'] else None
            if univis_lectures:
                if type(univis_lectures) is list:
                    for univis_lecture in univis_lectures:
                        lecture = self._extract_Lecture(univis_lecture, rooms_map, persons_map)
                        if lecture:
                            lectures.append(lecture)
                else:
                    lectures = [self._extract_Lecture(univis_lectures, rooms_map, persons_map)]

        lectures_map = self.get_univis_key_dict(lectures)
        for lecture in lectures:
            lecture.set_parent_lecture(lectures_map)
        return lectures

    def _extract_Lecture(self, univis_lecture: dict, rooms_map: dict, persons_map: dict) -> UnivISLecture:
        return UnivISLecture(univis_lecture, rooms_map, persons_map)

    # def extract_allocations(self, univis_data: dict) -> List[UnivISAllocation]:
    #     univis_person_c = UnivISPersonController()
    #     persons = univis_person_c.extract_persons(univis_data)
    #     persons_map = self.get_univis_key_dict(persons)
    #
    #
    #     rooms = univis_room_c._extract_rooms(univis_data)
    #     allocations = self.get_allocations_from_data(univis_data['UnivIS']['Allocation']) if 'Allocation' in univis_data[
    #         'UnivIS'] else []
    #     rooms_dict = self.get_univis_key_dict(rooms)
    #
    #     for allocation in allocations:
    #         allocation.rooms = [rooms_dict[id] for id in allocation.room_ids if id in rooms_dict]
    #     return allocations
    #
    # def get_allocations_from_data(self, allocations):
    #     return [UnivISAllocation(allocation) for allocation in allocations]

    def get_filtered_allocations(self, start_date, end_date, start_time, end_time) -> List[UnivISAllocation]:
        data = self.load_page(self._get_univis_api_url(start_date, end_date, start_time, end_time))
        return self.extract_allocations(data) if data else []
