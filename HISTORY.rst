=======
History
=======

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
