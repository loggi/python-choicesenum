-------
History
-------

0.6.0 (2019-09-05)
------------------

* Adding schematics contrib type ChoicesEnumType.
* Drop support for Django 1.6, 1.7, 1.8.



0.5.3 (2019-02-06)
------------------

* Fix Django migrations with default values for Django 1.7+.


0.5.2 (2019-01-18)
------------------

* Optimize member check and dynamic creation of `is_<name>` properties.


0.5.1 (2019-01-04)
------------------

* Fix readme RST (requires new Pypi upload).


0.5.0 (2019-01-04)
------------------

* Membership test (item in Enum) returning valid results for primitive values.
* New dict-like `.get` method able to return a default value (thanks @leandrogs).
* Django: Support Postgres array functions and queries (thanks @tomfa).
* Django: Support for deferring an enum field using `queryset.defer()` (thanks @noamkush).
* Django: 2.1 support.


0.4.0 (2018-07-13)
------------------

* Optimistic casting of inner types (thanks @gabisurita).
* Optional stdlib patch to automagic json serialization support.
* Add Python3.7 to the test matrix.


0.3.0 (2018-06-22)
------------------

* Official Django 2.0 support (0.2.2 just works fine too).
* ``ChoicesEnum`` sharing the same hash() as his value. Can be used to retrieve/restore items in dicts (`d[enum] == d[enum.value]`).

0.2.2 (2017-12-01)
------------------

* Fix: Support queries through `select_related` with no `None` value defined (thanks @klette).


0.2.1 (2017-09-30)
------------------

* Fix South migrations for Django 1.6.


0.2.0 (2017-09-11)
------------------

* ``ChoicesEnum`` items are comparable by their values (==, !=, >, >=, <, <=) (thanks @jodal).
* +``ChoicesEnum.values``: Returns all the Enum's raw values (eq: ``[x.value for x in Enum]``).

0.1.7 (2017-09-10)
------------------

* Fix: ``ChoicesEnum`` is now hashable (thanks @jodal).


0.1.6 (2017-09-08)
------------------

* Fix: Proxy ``__len__`` calls to the inner enum value.


0.1.5 (2017-09-05)
------------------

* +ChoicesEnum.description: Alias for `label`, allow enum descriptors to be used by Graphene.


0.1.4 (2017-08-28)
------------------

* Fix South migrations for Django 1.6.
* ``ChoicesEnum`` repr can be used to reconstruct an instance (``item == eval(repr(item))``).


0.1.3 (2017-08-28)
------------------

* Fix sdist not including sub-modules (django contrib).

0.1.2 (2017-08-27)
------------------

* README fixes and improvements.

0.1.0 (2017-08-27)
------------------

* First release on PyPI.
