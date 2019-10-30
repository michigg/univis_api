import os
from typing import List
from urllib.parse import urlencode, quote_plus

from controllers.controllers import UnivISController
from controllers.person_controller import UnivISPersonController
from controllers.room_controller import UnivISRoomController
from models.allocation_models import UnivISAllocation


class UnivISAllocationController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = os.environ.get("UNIVIS_API_ENDPOINT")

    def get_urls(self, args) -> List[str]:
        params = {"search": "allocations", "show": "xml"}
        if "start_date" in args and args["start_date"]:
            params['start'] = args["start_date"]
        if "end_date" in args and args["end_date"]:
            params['end'] = args["end_date"]
        if "start_time" in args and args["start_time"]:
            params['starttime'] = args["start_time"]
        if "end_time" in args and args["end_time"]:
            params['endtime'] = args["end_time"]

        urls = [f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}']
        print(urls)
        return urls

    def get_allocations(self, univis_data: dict) -> List[UnivISAllocation]:
        univis_person_c = UnivISPersonController()
        persons = univis_person_c.get_persons(univis_data)
        persons_map = self.get_univis_key_dict(persons)

        univis_room_c = UnivISRoomController()
        rooms = univis_room_c.extract_rooms(univis_data=univis_data, persons_map=persons_map)
        rooms_map = self.get_univis_key_dict(rooms)

        allocations = []
        if 'UnivIS' in univis_data:
            univis_allocations = univis_data['UnivIS']['Allocation'] if 'Allocation' in univis_data['UnivIS'] else None
            if univis_allocations:
                if type(univis_allocations) is list:
                    for univis_allocation in univis_allocations:
                        allocation = self._extract_allocation(univis_allocation, rooms_map, persons_map)
                        if allocation:
                            allocations.append(allocation)
                else:
                    allocations = [self._extract_allocation(univis_allocations, rooms_map, persons_map)]
        return allocations

    def _extract_allocation(self, univis_allocation: dict, rooms_map: dict, persons_map: dict) -> UnivISAllocation:
        return UnivISAllocation(univis_allocation, rooms_map, persons_map)

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
