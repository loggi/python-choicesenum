
def test_pytest_make_parametrize_id(testdir):
    testdir.makeconftest("")

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

    result.stdout.fnmatch_lines([
        "*test_param_repr[Color.RED*",
        "*test_param_repr[Color.GREEN*",
        "*test_param_repr[Color.BLUE*",
    ])
