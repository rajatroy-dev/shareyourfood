from typing import Dict


class Query:
    def find_nearby_entry(latitude: int, longitude: int) -> list[Dict[str, str]]:
        distance_in_metres: int = 1000
        query = 'SELECT e.username FROM ENTRIES e WHERE \
                    ST_DISTANCE(e.location, { \
                        "type": "Point", \
                        "coordinates" : [' + latitude + ', ' + longitude + '] \
                    }) < ' + distance_in_metres + \
                    'AND message_type = share'

        return query
