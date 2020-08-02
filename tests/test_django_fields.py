# coding: utf-8
from __future__ import absolute_import, unicode_literals

import mock

import pytest
import django

from choicesenum.django.fields import FieldErrors


@pytest.fixture(params=['string', 'integer'])
def field_type(request):
    return request.param


@pytest.fixture(params=[True, False], ids=['field_null', 'field_not_null'])
def field_allow_null(request):
    return request.param


@pytest.fixture(params=[True, False], ids=['enum_null', 'enum_not_null'])
def enum_allow_null(request):
    return request.param


@pytest.fixture(params=[True, False], ids=['with_default', 'without_default'])
def has_default(request):
    return request.param


@pytest.fixture
def string_field_cls():
    from choicesenum.django.fields import EnumCharField
    return EnumCharField


@pytest.fixture
def integer_field_cls():
    from choicesenum.django.fields import EnumIntegerField
    return EnumIntegerField


@pytest.fixture
def field_cls(request, field_type):
    fixture_name = '{}_field_cls'.format(field_type)
    return request.getfixturevalue(fixture_name)


@pytest.fixture()
def enum_for_field_cls(request, field_type, enum_allow_null):
    enum_by_type = {
        'string': ['colors', 'sizes'],
        'integer': ['http_statuses', 'user_statuses'],
    }
    fixture_options = enum_by_type[field_type]
    fixture_name = fixture_options[enum_allow_null]
    return request.getfixturevalue(fixture_name)


@pytest.fixture(params=['str_red', 'enum_red', 'str_green', 'enum_green'])
def color(request):
    from tests.app.enums import Color
    return {
        'str_red': Color.RED.value,
        'enum_red': Color.RED,
        'str_green': Color.GREEN.value,
        'enum_green': Color.GREEN,
    }.get(request.param)


@pytest.mark.django_db
def test_string_field_should_allow_creating_objects_with_values(color):
    # given
    from tests.app.models import ColorModel, Color
    enum_color = Color(color)

    # when
    instance = ColorModel.objects.create(color=color)

    # then
    assert instance.color.value == enum_color.value
    assert instance.color.display == enum_color.display


@pytest.mark.django_db
def test_should_allow_queryset_defer(color):
    # given
    from tests.app.models import ColorModel, Color
    enum_color = Color(color)
    ColorModel.objects.create(color=color)

    # when
    instance = ColorModel.objects.filter(color=color).defer('color').first()

    # then
    assert instance.color.value == enum_color.value
    assert instance.color.display == enum_color.display


@pytest.mark.django_db
def test_string_field_should_allow_assigning_values(color):
    # given
    from tests.app.models import ColorModel, Color
    enum_color = Color(color)

    # when
    instance = ColorModel()
    instance.color = color
    instance.save()

    # then
    assert instance.color.value == enum_color.value
    assert instance.color.display == enum_color.display

    instance2 = ColorModel.objects.first()

    # then
    assert instance2.color.value == enum_color.value
    assert instance2.color.display == enum_color.display


def test_should_allow_enum_as_a_path_to_class(field_cls, enum_for_field_cls):
    # given
    import_path = enum_for_field_cls._import_path()
    default_enum = enum_for_field_cls.options()[0]

    # when
    field = field_cls(
        enum=import_path,
        default=default_enum,
    )

    # then
    assert field.enum is enum_for_field_cls


@pytest.mark.skipif(django.VERSION[:2] < (1, 7), reason="requires Django 1.7+ for migrations")
def test_migrations_deconstruct_support(field_cls, enum_for_field_cls):
    default_enum = enum_for_field_cls.options()[0]
    field = field_cls(
        enum=enum_for_field_cls,
        default=default_enum,
    )
    assert field.deconstruct() == (
        None,
        'choicesenum.django.fields.{}'.format(field_cls.__name__),
        [],
        {
            'enum': enum_for_field_cls,
            'default': default_enum.value,
        },
    )


@pytest.mark.skipif(django.VERSION[:2] < (1, 7), reason="requires Django 1.7+ for migrations")
def test_migrations_deconstruct_support_without_enum(field_cls, enum_for_field_cls):
    field = field_cls(
        choices=enum_for_field_cls.choices(),
    )
    assert field.deconstruct() == (
        None,
        'choicesenum.django.fields.{}'.format(field_cls.__name__),
        [],
        {
            'choices': enum_for_field_cls.choices(),
        },
    )


# TODO: Attempt to turn field check tests compatible with Django 1.7
@pytest.mark.skipif(django.VERSION[:2] < (1, 8), reason="requires Django 1.7+ for field.check()")
class TestFieldChecks(object):

    def test_error_if_null_but_enum_didnt_allow_null(
            self, field_cls, enum_for_field_cls, field_allow_null, enum_allow_null):
        # given
        field = field_cls(
            enum=enum_for_field_cls,
            null=field_allow_null,
            default=enum_for_field_cls.options()[0]
        )
        expected_errors = [FieldErrors.E01] if field_allow_null and not enum_allow_null else []

        # when
        errors = field.check()

        # then
        assert [e.id for e in errors] == expected_errors

    def test_error_if_default_not_provided_value_is_not_supported(
            self, field_cls, enum_for_field_cls, enum_allow_null):
        # given
        field = field_cls(
            enum=enum_for_field_cls,
            null=False,
        )
        expected_errors = [FieldErrors.E02] if not enum_allow_null else []

        # when
        errors = field.check()

        # then
        assert [e.id for e in errors] == expected_errors


class TestCompatModule(object):

    def test_creator_should_call_field_to_python_on_assigment(self):
        from tests.app.models import User, UserStatus

        with mock.patch('choicesenum.django.fields.EnumFieldMixin.to_python') as m:
            m.return_value = UserStatus.DELETED

            # given
            instance = User()

            # when
            instance.status = UserStatus.ACTIVE

            # then
            m.assert_called_with(UserStatus.ACTIVE)
            assert instance.status == UserStatus.DELETED


@pytest.mark.django_db
def test_integer_field_should_allow_filters():
    # given
    from tests.app.models import User, UserStatus

    # when
    instance = User()
    instance.status = UserStatus.ACTIVE
    instance.save()

    User.objects.create(status=UserStatus.INACTIVE)

    # then
    assert instance.status.value == UserStatus.ACTIVE

    instance2 = User.objects.filter(status=UserStatus.ACTIVE).first()
    assert instance.pk == instance2.pk


def test_field_to_python_should_allow_inherited_conversion():
    # given
    from tests.app.models import User

    # when
    user_status = User._meta.get_field('status').to_python('1')

    # then
    assert user_status.is_pending


@pytest.mark.django_db
def test_handle_select_related_with_no_none_enum_value():
    # given
    from tests.app.models import Preference

    # when
    Preference.objects.create()

    # then

    objs = Preference.objects.select_related('color')
    assert len(objs) == 1


@pytest.mark.django_db
def test_converts_null_to_enum_none_if_present():
    # given
    from tests.app.models import User, UserStatus

    # when
    User.objects.create(status=None)
    instance = User.objects.filter(status=None).first()

    # then
    assert instance.status.display == UserStatus.UNDEFINED.display


@pytest.mark.django_db
def test_raise_error_when_value_is_not_an_possible_choice():
    # given
    from tests.app.models import User
    from django.db import connection
    cur = connection.cursor()
    try:
        cur.execute("insert into app_user values(1, 'bla', 5)")
    finally:
        cur.close()

    # when
    with pytest.raises(ValueError) as excinfo:
        User.objects.first()

    # then
    assert str(excinfo.value) == '5 is not a valid UserStatus'


@pytest.mark.skipif(
    django.VERSION[:2] < (1, 7),
    reason="requires Django 1.7+ for accessing Model.attribute.field")
def test_converts_list_aggregations():
    # given
    from tests.app.models import ColorModel, Color

    # when
    db_return_value = [Color.RED.value, Color.GREEN.value, None]

    # then
    objs = ColorModel.color.field.from_db_value(db_return_value, None, None, None)

    assert objs == [Color.RED, Color.GREEN]
