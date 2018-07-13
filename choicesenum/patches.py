

def patch_json():
    """
    Patch json default encoder to globally try to find and call a ``__json__``
    method inside classes before raising "TypeError: Object of type 'X' is not
    JSON serializable"
    """
    from json import JSONEncoder

    def _default(self, obj):
        return getattr(obj.__class__, "__json__", _default.default)(obj)

    _default.default = JSONEncoder().default
    JSONEncoder.default = _default
