
class GetTeamResponse:
    def __init__(self, team):
        self.team = team

    def toJSON(self) -> dict:
        return {
            'id': str(self.team.id),
            'name': self.team.name,
            'created_at': self.team.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
