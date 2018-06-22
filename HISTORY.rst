=======
History
=======

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
