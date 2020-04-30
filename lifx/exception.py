class AuthorizationException(Exception):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class LightNotFoundException(Exception):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message