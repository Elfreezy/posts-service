from fastapi import status


class ItemNotFoundError(Exception):
    def __init__(self, name):
        self.name = name
        self.status_code = status.HTTP_404_NOT_FOUND
