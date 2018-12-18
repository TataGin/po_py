def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
