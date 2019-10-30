from pprint import pprint


class UnivISBase:
    def _get_orgunits(self, univis_data):
        if "orgunits" in univis_data:
            if type(univis_data['orgunits']) is list:
                return [orgunit for orgunit in univis_data['orgunits']['orgunit']]
            return univis_data['orgunits']['orgunit']
        return []
