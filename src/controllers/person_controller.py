import os
from pprint import pprint
from typing import List

from controllers.controllers import UnivISController
from models.enums.building_key import BuildingKey
from models.enums.faculty import Faculty
from models.person_models import UnivISPerson
from urllib.parse import urlencode, quote_plus


class UnivISPersonController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = os.environ.get("UNIVIS_API_ENDPOINT")

    def get_url(self, args) -> str:
        # TODO: lehrtyp, xjob, path
        params = {"search": "persons", "show": "xml"}
        if "id" in args and args["id"]:
            params['id'] = args["id"]
        if "token" in args and args["token"]:
            params['fullname'] = args["token"]
        if "full_name" in args and args["full_name"]:
            params['fullname'] = args["full_name"]
        if "last_name" in args and args["last_name"]:
            params['name'] = args["last_name"]
        if "first_name" in args and args["first_name"]:
            params['longname'] = args["first_name"]
        if "title" in args and args["title"]:
            params['title'] = args["title"]
        print(f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}')
        return f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}'

    def get_univis_data_persons(self, urls):
        persons = []
        for url in urls:
            univis_data = self.load_page(url)
            persons.extend(self._extract_persons(univis_data))
        return persons

    def _extract_persons(self, univis_data: dict) -> List[UnivISPerson]:
        univis_persons = self._get_univis_persons_from_univis_data(univis_data=univis_data)
        persons = []
        if type(univis_persons) is list:
            for univis_person in univis_persons:
                person = self._extract_person(univis_person)
                if person:
                    persons.append(person)
        else:
            person = self._extract_person(univis_persons)
            persons.append(person)
        return persons

    def _extract_person(self, univis_person: dict) -> UnivISPerson or None:
        return UnivISPerson(univis_person)

    def _get_univis_persons_from_univis_data(self, univis_data: dict) -> List[dict] or None:
        if 'UnivIS' in univis_data:
            return univis_data['UnivIS']['Person'] if 'Person' in univis_data['UnivIS'] else None
        return None
