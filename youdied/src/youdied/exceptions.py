class YouDiedError(Exception):
    """
    Base class for module exceptions
    """


class CannotLoadCharacterError(YouDiedError):
    """Temporary Warning that should be removed"""

    def __init__(self):
        super(CannotLoadCharacterError, self).__init__(
            'Cannot load character for previous session. Is this your first time? Provide character name.'
        )
