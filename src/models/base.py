from pprint import pprint


class UnivISBase:
    def _get_orgunits(self, univis_data):
        if "orgunits" in univis_data:
            if type(univis_data['orgunits']) is list:
                return [orgunit for orgunit in univis_data['orgunits']['orgunit']]
            return univis_data['orgunits']['orgunit']
        return []

    def _get_contacts(self, univis_contacts, persons_map):
        if type(univis_contacts) is list:
            return [persons_map[univis_contact["UnivISRef"]['@key']] for univis_contact in univis_contacts]
        return [persons_map[univis_contacts["UnivISRef"]['@key']]]
