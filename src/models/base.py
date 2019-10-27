class UnivISBase:
    def _get_orgunits(self, univis_data):
        if len(univis_data['orgunits']) > 1:
            return [orgunit for orgunit in univis_data['orgunits']['orgunit']]
        return univis_data['orgunits']['orgunit']
