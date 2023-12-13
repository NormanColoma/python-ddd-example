from domain.team.team_repository import TeamRepository


class AddTeam:
    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def save(self) -> None:
        print('Saving team')
        # self.team_repository.save()
