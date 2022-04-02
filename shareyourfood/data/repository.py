from shareyourfood.data.model.location import Location


class Repository:
    def share_food(self, chat_id: int, username: str, message_id: int, location: Location = None):
        pass

    def find_entry(self, chat_id: int, username: str, message_id: int):
        pass

    def request_food(self, chat_id: int, username: str, message_id: int):
        pass

    def find_food(self, location: Location):
        pass
