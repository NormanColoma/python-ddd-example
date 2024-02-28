import uuid
from datetime import datetime
from uuid import UUID

import pytest

from src.domain.core.domain_entity import DomainEntity
from src.domain.core.invalid_domain_entity_error import InvalidDomainEntityError

id = uuid.UUID('1904b253-2fb4-44ea-a75e-6fee92dbe153')
created_at = datetime.now()


class Foo(DomainEntity):
    def __init__(self, id: UUID, created_at: datetime):
        if id is None and created_at is None:
            super().__init__()
        elif id is None:
            super().__init__(created_at=created_at)
        elif created_at is None:
            super().__init__(id=id)
        else:
            super().__init__(id, created_at)

    def to_object(self) -> dict:
        return super().to_object()


def test_should_raise_exception_while_instantiating_directly():
    with pytest.raises(TypeError):
        DomainEntity()


def test_should_raise_exception_when_id_is_not_uuid():
    with pytest.raises(InvalidDomainEntityError) as e:
        Foo(id='id', created_at=None)
    assert e.value.message == 'Field id must be a valid UUID type'


def test_should_raise_exception_when_created_at_is_not_date():
    with pytest.raises(InvalidDomainEntityError) as e:
        Foo(id, created_at='date')
    assert e.value.message == 'Field created_at must be a valid datetime type'


def test_should_build_domain_entity():
    foo = Foo(id, created_at)
    assert foo.id == id
    assert foo.created_at == created_at


def test_should_build_domain_entity_with_default_values():
    foo = Foo(None, None)
    assert foo.id is not None
    assert foo.created_at is not None


def test_to_object():
    foo = Foo(id, created_at)

    expect_dict = {
        'id': str(id),
        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    assert foo.to_object() == expect_dict
