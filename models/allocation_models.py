from enum import Enum


class Department(Enum):
    WIAI = "Fakultät Wirtschaftsinformatik"
    GUK = "Fakultät Geistes- und Kulturwissenschaften"



class Allocation:
    def __init__(self, univis_allocation: dict):
        self.univis_key = univis_allocation.get('@key', None)
        self.title = univis_allocation.get('title', None)
        self.start_date = univis_allocation.get('startdate', None)
        self.end_date = univis_allocation.get('enddate', None)
        self.start_time = univis_allocation.get('starttime', None)
        self.end_time = univis_allocation.get('endtime', None)
        self.orgname = univis_allocation.get('orgname', None)
        self.orgunits = self._init_orgunits(univis_allocation)
        self.contact = None
        self.room_ids = self._get_room_id(univis_allocation.get('rooms')) if univis_allocation.get('rooms',
                                                                                                   None) else ''
        self.rooms = []

    def _get_room_id(self, rooms):
        if 'UnivISRef' in rooms['room']:
            return [rooms['room']['UnivISRef']['@key']]
        else:
            return [room['UnivISRef']['@key'] for room in rooms['room']]

    def _init_orgunits(self, univis_room):
        if len(univis_room['orgunits']) > 1:
            return [orgunit for orgunit in univis_room['orgunits']['orgunit']]
        return univis_room['orgunits']['orgunit']

    def __str__(self):
        return f'Allocation {self.title} {self.start_date}-{self.end_date}\n\tTime {self.start_time}\n\tTitle {self.end_time}'