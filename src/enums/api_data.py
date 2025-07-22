from enum import Enum

class BaseRequest(Enum):

    BASE_URL = "https://restful-booker.herokuapp.com"
    HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

