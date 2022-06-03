import json
import os
from typing import Dict
from shareyourfood.data.model.location import PointLocation


class CosmosQuery:
    def find_nearby_food(latitude: int, longitude: int) -> str:
        distance_in_metres: str = os.getenv('SEARCH_RADIUS')
        location: PointLocation = PointLocation([latitude, longitude])
        dict_location: Dict = location.to_dict()
        str_location: str = json.dumps(dict_location)

        query = 'SELECT e.username FROM ENTRIES e WHERE' \
            ' ST_DISTANCE(e.location, ' + str_location + ') < ' + distance_in_metres + \
                ' AND e.message_type = "share"'

        return query

    def find_nearby_entry(chat_id: int, username: str, message_id: int) -> str:
        query = 'SELECT * FROM ENTRIES e WHERE' \
                ' e.chat_id = ' + str(chat_id) + \
                ' AND e.username = "' + username + '"' + \
                ' AND e.message_id = ' + str(message_id)

        return query
