from models.base import UnivISBase


class UnivISAllocation(UnivISBase):
    def __init__(self, univis_allocation: dict, rooms_map: dict, persons_map: dict):
        self.univis_key = univis_allocation.get('@key', None)
        self.title = univis_allocation.get('title', None)
        self.start_date = univis_allocation.get('startdate', None)
        self.end_date = univis_allocation.get('enddate', None)
        self.start_time = univis_allocation.get('starttime', None)
        self.end_time = univis_allocation.get('endtime', None)
        self.orgname = univis_allocation.get('orgname', None)
        self.orgunits = self._get_orgunits(univis_allocation)

        raw_univis_contact = univis_allocation['contact'] if 'contact' in univis_allocation else None
        self.contact = self._get_contacts(raw_univis_contact, persons_map)[0] if raw_univis_contact else None

        raw_univis_rooms = univis_allocation['rooms']['room'] if 'rooms' in univis_allocation else None
        self.rooms = self._get_rooms(raw_univis_rooms, rooms_map) if raw_univis_rooms else None

    def _get_rooms(self, univis_rooms, rooms_map):
        if type(univis_rooms) is list:
            return [rooms_map[univis_room["UnivISRef"]['@key']] for univis_room in univis_rooms if
                    univis_room["UnivISRef"]['@key'] in rooms_map]
        return [rooms_map[univis_rooms["UnivISRef"]['@key']]] if univis_rooms["UnivISRef"][
                                                                     '@key'] in rooms_map else []

    def __str__(self):
        return f'Allocation {self.title} {self.start_date}-{self.end_date}\n\tTime {self.start_time}\n\tTitle {self.end_time}'
