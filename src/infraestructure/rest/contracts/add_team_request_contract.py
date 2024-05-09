class AddTeamRequestContract:
    @staticmethod
    def contract() -> dict:
        return {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
            },
            'required': ['name']
        }
