from application.repository import Repository


class UseCase:
    def __init__(self, repository: Repository):
        self.repository = repository

    def save(self):
        return self.repository.save()
