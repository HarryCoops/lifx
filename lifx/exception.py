class AuthorizationException(Exception):
    """
    Exception raised when a session is provided an invalid token.
    """

    def __init__(self, token: str):
        self.message = f"Authorization failed for token {token}"
        super().__init__(self.message)
