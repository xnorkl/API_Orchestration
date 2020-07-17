import pp

# Higher Order Functions
def isiterable(obj):
    """ Check if an object is iterable. If not, ask forgiveness. """
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True


def member(a, b):
    """ Takes a value a & returns if a is an element of b. """
    if a in set(elem.value for elem in b):
        return a
    else:
        raise TypeError('{} is not a member of {}'.format(a, b))


def ismember(m, f, a):
    """
    Take a function f, and api a in module m.
    Return True or False if f of m is a member of a.
    """
    if member(f, evoke(m, a)):
        return True
    else:
        return False


def evoke(m, o):
    """
    Takes a string m and o, & returns a matching object in module m.
    """
    return getattr(globals()[m], o)


def helper(f, args):
    """
    Helper takes a function f and an object args and returns f(args).

    Helper tries to determine first how to unpack if args are an iterable.
    If args are not iterable, helper casts args to list to then unpack.
    This allows for avoiding passing a single argument as an iterable.

    """
    try:
        if callable(f):
            if isinstance(args, list) or isinstance(args, tuple):
                return f(*args)
            if isinstance(args, dict):
                return f(**args)
        else:
            return f(args)
    except Exception as e:
        print(e)


def call(m, f, *args):
    """
    Takes a module, function, and *args & returns f(*args).
    """
    return helper(evoke(m, f), *args)
