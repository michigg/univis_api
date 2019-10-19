from typing import List
from urllib.parse import urlencode, quote_plus

from utils.controllers import UnivISController
from models.allocation_models import Allocation


class UnivISAllocationController(UnivISController):
    def __init__(self):
        UnivISController.__init__(self)
        self.univis_api_base_url = "http://univis.uni-bamberg.de/prg"

    def _get_univis_api_url(self, start_date, end_date, start_time, end_time):
        params = {"search": "allocations", "show": "xml"}
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
        if start_time:
            params['starttime'] = start_time
        if end_time:
            params['endtime'] = end_time
        url = f'{self.univis_api_base_url}?{urlencode(params, quote_via=quote_plus)}'
        return url

    def get_allocations(self, data: dict) -> List[Allocation]:
        rooms = self.get_rooms_from_data(data['UnivIS']['Room']) if 'Room' in data['UnivIS'] else []
        allocations = self.get_allocations_from_data(data['UnivIS']['Allocation']) if 'Allocation' in data[
            'UnivIS'] else []
        rooms_dict = self.get_univis_key_dict(rooms)

        for allocation in allocations:
            allocation.rooms = [rooms_dict[id] for id in allocation.room_ids if id in rooms_dict]
        return allocations

    def get_allocations_from_data(self, allocations):
        return [Allocation(allocation) for allocation in allocations]

    def get_filtered_allocations(self, start_date, end_date, start_time, end_time) -> List[Allocation]:
        data = self.load_page(self._get_univis_api_url(start_date, end_date, start_time, end_time))
        return self.get_allocations(data) if data else []
