import pytest

from random import randint

from backup_service.database import one_c_bases

from tests.utils.common_fixtures import preload_database
from tests.utils.generators import random_string


@pytest.fixture()
def set_testing_one_c_base():
    def set_one_c_base(base_name: str = f'{randint(100, 999)}_{random_string(10)}') -> one_c_bases.OneCBases:
        return one_c_bases.OneCBases.set_or_get(original_name=base_name, alias_name=base_name, share=True)

    return set_one_c_base


def test_set_one_c_base(set_testing_one_c_base):
    base_name_payload = f"{randint(100, 999)}_{random_string(10)}"

    set_one_c_base = set_testing_one_c_base(base_name=base_name_payload)

    assert isinstance(set_one_c_base, one_c_bases.OneCBases)
    assert set_one_c_base.original_name == base_name_payload
    assert set_one_c_base.alias_name == base_name_payload


@pytest.mark.parametrize('invalid_name', [None])
def test_set_invalid_one_c_base(invalid_name):
    with pytest.raises(ValueError):
        one_c_bases.OneCBases.set_or_get(**{'original_name': invalid_name, 'alias_name': invalid_name, 'share': False})


def test_get_one_c_bases(set_testing_one_c_base):
    set_one_c_base = set_testing_one_c_base()

    get_one_c_bases = one_c_bases.OneCBases.get_all(
        id=set_one_c_base.id,
        original_name=set_one_c_base.original_name,
        alias_name=set_one_c_base.alias_name,
        share=set_one_c_base.share
    )
    for one_c_base in get_one_c_bases:
        assert set_one_c_base.id == one_c_base.id
        assert set_one_c_base.original_name == one_c_base.original_name
        assert set_one_c_base.alias_name == one_c_base.alias_name
        assert set_one_c_base.share == one_c_base.share


@pytest.mark.parametrize('one_c_base_data', [
    {'id': -1},
    {'id': None},
    {'original_name': ''},
    {'original_name': 0},
    {'original_name': None},
    {'alias_name': ''},
    {'alias_name': 0},
    {'alias_name': None},

])
def test_get_non_existent_one_c_bases(one_c_base_data):
    get_one_c_bases = one_c_bases.OneCBases.get_all(**one_c_base_data)

    assert get_one_c_bases == []


def test_get_last_one_c_base(set_testing_one_c_base):
    set_one_c_base = set_testing_one_c_base()

    get_last_one_c_base = one_c_bases.OneCBases.get_last(
        id=set_one_c_base.id,
        original_name=set_one_c_base.original_name,
        alias_name=set_one_c_base.alias_name,
        share=set_one_c_base.share
    )

    assert set_one_c_base.id == get_last_one_c_base.id
    assert set_one_c_base.original_name == get_last_one_c_base.original_name
    assert set_one_c_base.alias_name == get_last_one_c_base.alias_name
    assert set_one_c_base.share == get_last_one_c_base.share


@pytest.mark.parametrize('one_c_base_data', [
    {'id': -1},
    {'id': None},
    {'original_name': ''},
    {'original_name': 0},
    {'original_name': None},
    {'alias_name': ''},
    {'alias_name': 0},
    {'alias_name': None},
])
def test_get_non_existent_one_c_base(one_c_base_data):
    get_last_one_c_base = one_c_bases.OneCBases.get_last(**one_c_base_data)

    assert get_last_one_c_base is None


@pytest.mark.parametrize('field_update', [
    {'original_name': random_string(16)},
    {'original_name': 0},
    {'alias_name': random_string(16)},
    {'alias_name': 0},
    {'share': False},
    {'original_name': random_string(16), 'alias_name': random_string(16), 'share': False}
])
def test_update_fields(set_testing_one_c_base, field_update):
    set_base = set_testing_one_c_base()

    one_c_base_updated_alias = set_base.update(field_update)

    for field_key, field_value in field_update.items():
        assert one_c_base_updated_alias.__dict__.get(field_key) == field_value
