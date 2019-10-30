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

    def get_urls(self, args) -> List[str]:
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
        return [f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}']

    def get_persons(self, univis_data: dict) -> List[UnivISPerson]:
        univis_persons = None
        if 'UnivIS' in univis_data:
            univis_persons = univis_data['UnivIS']['Person'] if 'Person' in univis_data['UnivIS'] else []
        if univis_persons:
            persons = []
            if type(univis_persons) is list:
                for univis_person in univis_persons:
                    person = UnivISPerson(univis_person)
                    if person:
                        persons.append(person)
            else:
                person = UnivISPerson(univis_persons)
                persons.append(person)
            return persons
        return []
