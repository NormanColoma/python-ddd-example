import uuid
from datetime import datetime
from uuid import UUID
import pytest

from src.domain.core.aggregate_root import AggregateRoot
from src.domain.core.bus.event.domain_event import DomainEvent


class Foo(AggregateRoot):
    def __init__(self, id: UUID, created_at: datetime):
        super().__init__(id, created_at)

    def to_dict(self) -> dict:
        pass


class TestAggregateRoot:
    id = uuid.uuid4()
    created_at = datetime.now()

    def test_should_raise_exception_while_instantiating_directly(self):
        with pytest.raises(TypeError):
            AggregateRoot()

    def test_should_pull_events(self):
        foo = Foo(self.id, self.created_at)

        assert len(foo.pull_events()) == 0

    def test_should_add_event(self):
        class Event(DomainEvent):
            def __init__(self):
                pass

        foo = Foo(self.id, self.created_at)
        foo.add_event(Event())
        assert len(foo.pull_events()) == 1
        assert len(foo.pull_events()) == 0

    def test_should_not_add_event_when_is_not_a_domain_event(self):
        class Event:
            def __init__(self):
                pass

        foo = Foo(self.id, self.created_at)
        foo.add_event(Event())
        assert len(foo.pull_events()) == 0
