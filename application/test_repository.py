from application.repository import Repository


class TestRepository(Repository):
    def save(self) -> str:
        return "Hello from save"
