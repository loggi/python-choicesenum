# coding: utf-8

import pytest


@pytest.fixture
def colors():
    from tests.app.enums import Color
    return Color


@pytest.fixture
def http_statuses():
    from tests.app.enums import HttpStatus
    return HttpStatus


@pytest.fixture
def user_statuses():
    from tests.app.enums import UserStatus
    return UserStatus


@pytest.fixture
def sizes():
    from tests.app.enums import Sizes
    return Sizes
