import json
import os
from shareyourfood.data.model.location import Location


class CosmosQuery:
    def find_nearby_food(latitude: int, longitude: int) -> str:
        distance_in_metres: int = os.getenv('SEARCH_RADIUS')
        location: Location = Location(type='Point',
                                      coordinates=[latitude, longitude])
        dict_location: dict = location.to_dict()
        str_location: str = json.dumps(dict_location)

        query = 'SELECT e.username FROM ENTRIES e WHERE' \
                    ' ST_DISTANCE(e.location, '  + str_location + ') < ' + distance_in_metres + \
                ' AND e.message_type = share'

        return query

    def find_nearby_entry(chat_id: int, username: str, message_id: int) -> str:
        query = 'SELECT * FROM ENTRIES e WHERE' \
                ' e.chat_id = ' + chat_id + \
                ' AND e.username = ' + username + \
                ' AND e.message_id = ' + message_id

        return query
