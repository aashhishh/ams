import os
import pathlib
from app.config import Config


class Setting:
    # The fill path of this repository

      # Request Headers
    API_KEY_HEADER_KEY = 'x-api-key'
    TOKEN_HEADER_KEY = 'x-auth-token'
    HEADERS = {'Content-Type': 'application/json'}
    MAX_RETRY = 2