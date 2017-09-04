import pytest

from choicesenum import ChoicesEnum


def django_16():
    try:
        import django
        return django.VERSION[:2] == (1, 6)
    except:
        return False


class Color(ChoicesEnum):
    RED = '#f00', 'Vermelho'
    GREEN = '#0f0', 'Verde'
    BLUE = '#00f', 'Azul'


@pytest.mark.skipif(
    django_16(), reason="Django 1.6 requires a pytest-django that crashes on tearddown")
def test_pytest_make_parametrize_id(testdir):
    testdir.makepyfile("""
        import pytest
        from choicesenum import ChoicesEnum

        @pytest.fixture
        def django_test_environment():
            # To hide the error:
            "RuntimeError: setup_test_environment() was already called and"
            "can't be called again without first calling teardown_test_environment()"
            pass

        class Color(ChoicesEnum):
            RED = '#f00', 'Vermelho'
            GREEN = '#0f0', 'Verde'
            BLUE = '#00f', 'Azul'

        @pytest.mark.parametrize("color", Color)
        def test_param_repr(color):
            assert color == color.value
    """)
    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines_random([
        "*test_param_repr[Color.RED*",
        "*test_param_repr[Color.GREEN*",
        "*test_param_repr[Color.BLUE*",
    ])


@pytest.mark.parametrize('color', Color)
def test_pytest_using_enum_as_fixture(color):
    assert color == color.value
