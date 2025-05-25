from src.application.application_response import ApplicationResponse


class GetTeamResponse(ApplicationResponse):
    def __init__(self, team):
        self.team = team

    def to_json(self) -> dict:
        return {
            "id": str(self.team.id),
            "name": self.team.name,
            "created_at": self.team.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "players": [
                {"name": player.name, "created_at": player.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                for player in self.team.players
            ],
        }
