class AuthorizationException(Exception):
    def __init__(self, token: str):
        self.message = f"Authorization failed for token {token}"
        super().__init__(self.message)
