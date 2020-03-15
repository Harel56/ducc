parsers = {}


def run_parser(name, data):
    """Runs parser with name that matches the argument 'name'
    on input given by argument 'data' and returns its result"""
    return parsers[name](data)


def parser(name='', parser=None):
    """ Decorator for adding parsers.
    optional argument name is used to determine the parsers name,
    it's also used as the topic said parser's result is published to.
    If argument name is not specified then the function's name is used.
    It's also possible to give the function of the parser as the
    optional argument parser instead of using this as a decorator."""
    def decorator(parser):
        parsers[name or parser.__name__] = parser
        return parser
    return decorator if parser is None else decorator(parser)
